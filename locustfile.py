import base64

from locust import HttpUser, TaskSet, task, between
from random import randint, choice


class WebTasks(HttpUser):
    wait_time = between(1, 2)

    @task
    def load(self):
#        base64string = base64.encodebytes(bytes(('%s:%s' % ('user', 'password')).replace('\n', ''), encoding = 'utf-8'))
        usrPass = "user:password"
#        b64Val = base64.b64encode(usrPass)
        encoded_u = base64.b64encode(usrPass.encode()).decode()

        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("/")
        self.client.get("/login", headers={"Authorization":"Basic %s" % encoded_u})
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")


# class Web(HttpUser):
    
#     task_set = WebTasks
#     min_wait = 0
#     max_wait = 0
