import os
import sys
import time
from datetime import datetime
from itertools import chain
from pathlib import Path
from typing import Any, Iterator, NoReturn, Optional, Union

import requests
from requests import exceptions
from retry import retry

CLASH_GIT_PATH = (
    "https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml"
)
CLASH_LOCAL_PATH_RELATIVE = f".config/clash/{datetime.now().strftime('%m%d%H%M')}.yaml"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
}

EXCEPTIONS = (
    exceptions.RequestException,
    exceptions.ConnectionError,
    exceptions.ConnectTimeout,
    exceptions.HTTPError,
    exceptions.Timeout,
    exceptions.SSLError,
    Exception,
)


T_Path = Union[Path, str]


def make_config_directory(specify_dir: Optional[str] = None) -> T_Path:
    def make_path(root_p: str) -> T_Path:
        path = Path(root_p).joinpath(CLASH_LOCAL_PATH_RELATIVE)
        Path(path.parent).mkdir(exist_ok=True, parents=True)
        return path

    if specify_dir:
        return make_path(specify_dir)
    else:
        if (
            (home_dir := Path("~").expanduser())
            or (home_dir := Path().home())
            or (home_dir := getattr(os.environ, "HOME", ""))
        ):
            return make_path(home_dir)
        else:
            raise FileNotFoundError(f"yaml路径不存在!")


@retry(exceptions=EXCEPTIONS, tries=3, delay=2)
def read_clash() -> Optional[Iterator]:
    # When stream=True is set on the request,
    # this avoids reading the content at once into memory for large responses.
    response = requests.get(CLASH_GIT_PATH, stream=True, headers=HEADERS)

    if response.status_code == 200:
        content = response.iter_content(chunk_size=128, decode_unicode=True)
        return content

    return None


def write_to_local_file(content: Iterator[Any]) -> NoReturn:
    # 校验是否为空
    try:
        first = next(content)
    except StopIteration:
        print("Remote-clash.yaml is empty!!!")
        sys.exit(1)
    else:
        new_content = chain(first, content)

        try:
            time_s = time.time()
            with open(make_config_directory(), "w") as f:
                f.writelines(new_content)
                print(
                    f"Write done! \nTime elapsed on writing file: {time.time() - time_s} s."
                )
                sys.exit(0)
        except Exception as e:
            print("Error: ", e)
            sys.exit(1)


if __name__ == "__main__":
    content = read_clash()
    write_to_local_file(content)
