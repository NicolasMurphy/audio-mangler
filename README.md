# Audio Mangler

`pip install -r requirements.txt`

`python app.py`

Added UV for python package management to be platform agnostic. 

UPDATE 9/10/25 
**use this command to exec program**
```uv run python app.py input_folder output_folder/output.wav```
 
 **Summary:**

- Use `uv add numpy scipy` inside a project to add them permanently.
- Use `uv run numpy scipy` for a quick scratch environment.   
- `uv` replaces the need for `pip install ...` + `venv` setup.

 **using [uv](https://github.com/astral-sh/uv)** (the fast Python package manager from Astral, successor to `pip`) to install libraries like **NumPy** and **SciPy**. Here’s how you can do it step by step:

## 🔹 1. Install `uv`

If you haven’t already installed it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

This will place the `uv` binary in `~/.cargo/bin/uv` by default. You can then add it to your PATH:

```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

(You may want to add that line to your `~/.bashrc` or `~/.zshrc` so it persists.)

You can verify it’s installed with:

```bash
uv --version
```
## 🔹 2. Initialize a Project (optional)

If you want a managed project:

```bash
uv init myproject
cd myproject
```
This creates a `pyproject.toml` and a `uv.lock`.

## 🔹 3. Install Packages (like NumPy, SciPy)

From inside your project folder:
```bash
uv add numpy scipy
```

This will:

- Add `numpy` and `scipy` to your `pyproject.toml` dependencies.
- Resolve and lock exact versions in `uv.lock`.
- Create a `.venv/` automatically (by default).    
- Install everything there.

## 🔹 4. Using Packages

Activate the virtual environment:

```bash
source .venv/bin/activate   # Linux/macOS
```
(or `.\.venv\Scripts\activate` on Windows PowerShell)

Then you can run:

```bash
python -c "import numpy as np; import scipy; print(np.__version__, scipy.__version__)"
```
## 🔹 5. Installing Without a Project (global or ad-hoc)

If you just want to quickly install something in a temporary environment:

```bash
uv run numpy scipy
```

That will create a temp venv, install `numpy` and `scipy`, and drop you into a Python REPL with them available. Great for quick experiments.

---



```bash
#run app
uv run python app.py
