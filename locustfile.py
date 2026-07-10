from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def load_main(self):
        self.client.get("/")
    
    @task
    def load_demografia(self):
        self.client.get("/?page=Perfil_Demográfico")
    
    @task
    def load_factores(self):
        self.client.get("/?page=Factores_de_Riesgo")