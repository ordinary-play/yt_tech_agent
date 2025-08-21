import os
from datetime import datetime
from fetch_trends import fetch_all_trends
from generate_script import generate_script_for
from storage import init_db, save_script

OUTPUT_DIR = "outputs"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def export_script_to_file(script_text, topic, sid):
    ensure_output_dir()
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (" ", "_")).rstrip()
    filename = f"{OUTPUT_DIR}/{sid}_{safe_topic[:50].replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Topic: {topic}\nGenerated at: {datetime.now()}\n\n")
        f.write(script_text)
    return filename
def run_agent(topic=None):
    if topic:
        chosen_topic = topic
        print(f"Using custom topic: {chosen_topic}")
    else:
        print("Fetching trending topics...")
        topics = fetch_all_trends()
        if not topics:
            print("No topics found.")
            return
        chosen_topic = topics[0]
        print(f"Chosen trending topic: {chosen_topic}")

    script_text = generate_script_for(chosen_topic)

    conn = init_db("data.db")
    sid = save_script(conn, chosen_topic, {"title": chosen_topic, "script": script_text})
    conn.close()

    file_path = export_script_to_file(script_text, chosen_topic, sid)

    result = {
        "id": sid,
        "topic": chosen_topic,
        "script": script_text,
        "file": file_path
    }
    return result



if __name__ == "__main__":
    run_agent()
