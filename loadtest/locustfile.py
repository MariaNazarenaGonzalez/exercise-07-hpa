# TODO: Locust load test
# from locust import HttpUser, task
# Hit /health and /api/nodes endpoints

import random
from locust import HttpUser, between, task

# Nombres de nodos para usar en los tests
NODE_NAMES = [f"node-{i}" for i in range(1, 50)]

class APIUser(HttpUser):
    # Espera entre 0.5 y 2 segundos entre tasks (simula usuario real)
    wait_time = between(0.5, 2)

    def on_start(self):
        """Se ejecuta una vez cuando el usuario virtual 'arranca'."""
        # Registramos un nodo propio para este usuario
        self.my_node = f"node-locust-{random.randint(1000, 9999)}"
        self.client.post("/api/nodes", json={
            "name": self.my_node,
            "host": "10.0.0.1",
            "port": 8080
        })

    @task(5)          # peso 5: se ejecuta 5x más que las de peso 1
    def health_check(self):
        """Endpoint liviano, genera volumen de requests."""
        self.client.get("/health")

    @task(3)
    def list_nodes(self):
        """GET /api/nodes — lectura de todos los nodos."""
        self.client.get("/api/nodes")

    @task(2)
    def get_my_node(self):
        """GET /api/nodes/{name} — lectura de un nodo específico."""
        self.client.get(f"/api/nodes/{self.my_node}")

    @task(1)
    def update_my_node(self):
        """PUT /api/nodes/{name} — escritura, más costosa."""
        self.client.put(f"/api/nodes/{self.my_node}", json={
            "host": f"10.0.{random.randint(0,255)}.{random.randint(1,254)}"
        })