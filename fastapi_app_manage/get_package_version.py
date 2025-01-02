
import requests
import concurrent.futures
from typing import List, Dict, Optional


def get_latest_package_version(package: str) -> Optional[str]:
    try:
        url = f"https://pypi.org/pypi/{package}/json"
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        latest_version = data["info"]["version"]
        return latest_version
    except requests.RequestException as e:
        print(f"Error fetching {package}: {e}")
        return None


def get_package_versions(packages: List[str]) -> Dict[str, Optional[str]]:
    versions = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_package = {executor.submit(get_latest_package_version, package): package for package in packages}
        for future in concurrent.futures.as_completed(future_to_package):
            package = future_to_package[future]
            try:
                version = future.result()
                versions[package] = version
            except Exception as exc:
                print(f"{package} generated an exception: {exc}")
                versions[package] = None
    return versions