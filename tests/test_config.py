from kml_viruswgs import get_threads_dict, get_conda_env_dict, get_database_dict, get_software_dict


def test_config():
    print(get_threads_dict())
    print(get_conda_env_dict())
    print(get_database_dict())
    print(get_software_dict())
