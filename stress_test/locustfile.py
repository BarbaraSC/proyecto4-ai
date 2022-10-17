from locust import HttpUser, task, between



class APIUser(HttpUser):

    # Put your stress tests here.
    # See https://docs.locust.io/en/stable/writing-a-locustfile.html for help.
    # TODO

    
    @task(1)
    def home(self):
        """
        request to home page
        """
        self.client.get("/")

    @task(4)
    def predict(self):
        """
        request to predict endpoint
        """
        data = {"file": open("dog.jpeg", "rb")}
        self.client.post("/predict", files=data)

    wait_time = between(1, 5)
  
    