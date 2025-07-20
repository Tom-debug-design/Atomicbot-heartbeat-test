
import os
import time
from git import Repo

# Miljøvariabel for GitHub-token
token = os.getenv("GITHUB_TOKEN")
if not token:
    print("❌ Feil: GITHUB_TOKEN er ikke satt!")
    exit(1)

# Repo-URL med token
repo_url = f"https://x-access-token:{token}@github.com/Tom-debug-design/Atomicbot-heartbeat-test.git"
local_path = "repo"
INTERVAL = 3600  # 1 time

# Klon repo hvis det ikke finnes lokalt
try:
    if not os.path.exists(local_path):
        print("📥 Kloner hovedrepo...")
        Repo.clone_from(repo_url, local_path)
except Exception as e:
    print(f"❌ Feil ved kloning: {e}")
    exit(1)

# Start loop for å pushe heartbeat
print("✅ Agent kjører. Starter heartbeat-loop...")
while True:
    try:
        filepath = os.path.join(local_path, "heartbeats.txt")
        with open(filepath, "a") as f:
            f.write(f"✅ Heartbeat: {time.ctime()}\n")

        repo = Repo(local_path)
        repo.git.add("heartbeats.txt")
        repo.index.commit("✅ Auto-heartbeat")
        origin = repo.remote(name="origin")
        origin.push()
        print("📤 Push utført!")
    except Exception as e:
        print(f"❌ Push-feil: {e}")
    time.sleep(INTERVAL)
