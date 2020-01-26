from app_controllers.services.kubernetes_controller import KubernetesController

kc = KubernetesController()

def test_setPodId():
    assert kc.setPodId("podid") == True