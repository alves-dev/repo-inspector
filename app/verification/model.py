class RepoVerificationResult:

    def __init__(self, key: str, description: str, passed: bool):
        self.key = key
        self.description = description
        self.passed = passed

    @classmethod
    def of_passed(cls, key: str, description: str):
        return cls(key, description, True)

    @classmethod
    def of_failure(cls, key: str, description: str):
        return cls(key, description, False)
