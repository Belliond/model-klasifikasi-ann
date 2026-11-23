import sys, importlib

def ver(name, attr="__version__"):
    try:
        m = importlib.import_module(name)
        return f"OK    {name:<16} {getattr(m, attr, '')}"
    except Exception as e:
        return f"FAIL  {name:<16} {type(e).__name__}: {e}"

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("-" * 60)
for pkg in ["numpy", "pandas", "sklearn", "scipy", "matplotlib",
            "seaborn", "imblearn", "openpyxl", "joblib", "tqdm"]:
    print(ver(pkg))

print("-" * 60)
try:
    import tensorflow as tf
    print(f"OK    tensorflow       {tf.__version__}")
    print(f"      Keras            {tf.keras.__version__}")
    print(f"      GPU tersedia     {len(tf.config.list_physical_devices('GPU')) > 0}")
except Exception as e:
    print(f"FAIL  tensorflow       {type(e).__name__}: {e}")

print("-" * 60)
for pkg in ["jupyter", "jupyterlab", "nbformat", "nbconvert", "ipykernel"]:
    print(ver(pkg))
