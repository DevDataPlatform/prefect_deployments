from prefect import flow
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_shell import shell_run_command
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

@flow(name="github-pull")
def pull_dost_github_repo():
        if Path('dbt').is_dir():
            shell_run_command('cd dbt && git pull')
        else:
            shell_run_command('rm -rf dbt && git clone '+ os.getenv('DOST_GITHUB_URL'))
        return 1

@flow(name='dbt-deps')
def run_dbt_deps():
    trigger_dbt_cli_command(
        command="dbt deps", project_dir='dbt'
    )
    return 1

@flow(name='dbt-source-snapshot-freshness')
def run_dbt_source_snapshot_freshness():
    trigger_dbt_cli_command(
        command="dbt source snapshot-freshness", project_dir='dbt'
    )
    return 1

@flow(name='dbt-run')
def run_dbt_run():
    trigger_dbt_cli_command(
        command="dbt run", project_dir='dbt'
    )
    return 1

@flow(name='dbt-test')
def run_dbt_test():
    trigger_dbt_cli_command(
        command="dbt test", project_dir='dbt'
    )
    return 1

@flow(name='generate-docs')
def generate_dbt_docs():
    trigger_dbt_cli_command(
        command="dbt docs generate", project_dir='dbt'
    )

    return 1

@flow(name="dbt-transform")
def run_dbt_transform():
    
    pull_dost_github_repo()

    run_dbt_deps()

    generate_dbt_docs()

    run_dbt_source_snapshot_freshness()

    run_dbt_run()

    run_dbt_test()
    
    return 1