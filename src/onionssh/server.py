from typing import List, Optional

from .bootstrap import check_dependencies


# TODO functionality as mixins
class Server:
    def get_deps(self) -> List[str]:
        return ["tor", "sshd"]

    def __init__(self, deps: Optional[List[str]] = None):
        if not deps:
            deps = self.get_deps()
        check_dependencies(deps)


if __name__ == "__main__":
    Server()
