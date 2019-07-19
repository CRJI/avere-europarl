job "scraper" {
  datacenters = ["dc1"]
  type = "batch"

   group "scraper" {
    task "scraper" {
      driver = "docker"
      config {
        image = "liquidinvestigations/crji-avere-europarl"
        command = "/app/scraper/main.py"

        volumes = [
          "/home/mihai/data:/app/scraper/data",
        ]
      }
      resources {
        memory = 256
        cpu = 2000
      }
    }
  }
}
