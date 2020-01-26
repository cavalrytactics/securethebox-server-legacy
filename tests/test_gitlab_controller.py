from app_controllers.services.gitlab_controller import GitlabController

gc = GitlabController()

def test_setClusterName():
    assert gc.setClusterName("clusterName") == True