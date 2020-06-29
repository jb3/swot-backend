print("=== IMPORTING PIP ===")

try:
    import pip._internal
except ModuleNotFoundError:
    print("PIP is not installed, please contact Joseph for more information")
    input()
    exit()

print("=== ATTEMPTING INSTALL ===")
try:
    pip._internal.main(
        [
            "install",
            "-r",
            "requirements.txt",
            "-r",
            "requirements-ci.txt"
        ]
    )
except Exception as e:
    print("Could not install through PIP")
    print(e)
    input()
    exit()

print("\n" * 3)
print("INSTALLATION COMPLETE!")
print("You can now run start_app.py")
input()