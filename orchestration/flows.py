import subprocess

from prefect import flow, task


@task
def run_training_script():
    """
    Run the main training script as a subprocess.

    Using a subprocess is a straightforward way to wrap existing scripts
    into a Prefect task without refactoring the script's internal logic.
    """
    print("Running the main training script...")
    # 'pipenv run' ensures this subprocess executes within the project's
    # virtual environment, using the correct dependencies.

    subprocess.run(["pipenv", "run", "python", "src/train.py"], check=True)
    print("Training script finished successfully.")


@flow(name="MVP Training Flow")
def mvp_training_flow():
    """
    Orchestrates the model training process.
    """
    run_training_script()


if __name__ == "__main__":
    mvp_training_flow()
