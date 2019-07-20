job "scraper-cron" {
  datacenters = ["dc1"]
  type = "batch"
  periodic {
    cron = "@daily"
    prohibit_overap = true
  }

   group "scraper" {
    count = 3
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
        cpu = 600
      }
    }
  }
}
