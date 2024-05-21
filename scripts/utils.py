import pandas as pd
from pathlib import Path

def get_base_path():
    base_path = Path(__file__).resolve().parent.parent
    return base_path

def get_ledger_path():
    ledger_path = str(Path(Path(__file__).resolve().parent.parent)/ "reports/masterLedger.csv")
    return ledger_path

def get_stdlibs_path():
    path = str(Path(Path(__file__).resolve().parent.parent)/ "scripts/pythonstandardlibs.csv")
    return path

def get_classification_report(git_url):
    git_url = git_url.replace(".git", "")
    df = pd.read_csv(get_ledger_path())
    uuid = df[df['repoUrl'] == git_url]['uuid'].values[0]
    base_path = get_base_path() 
    classification_report_path = base_path / "reports" / "classification_reports" / uuid / "fileClassificationReport.csv"
    return classification_report_path

def get_directory_report(git_url):
    git_url = git_url.replace(".git", "")
    df = pd.read_csv(get_ledger_path())
    uuid = df[df['repoUrl'] == git_url]['uuid'].values[0]
    base_path = get_base_path() 
    directory_report_path = base_path / "reports" / "classification_reports" / uuid / "directoryStructure.csv"
    return directory_report_path

def get_requirements_file(git_url):
    git_url = git_url.replace(".git", "")
    df = pd.read_csv(get_ledger_path())
    uuid = df[df['repoUrl'] == git_url]['uuid'].values[0]
    base_path = get_base_path() 
    requirements_file_path = base_path / "repos" / uuid / "requirements.txt"
    return requirements_file_path