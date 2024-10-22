from flask import Flask, jsonify, request
from db_instance import get_db

app = Flask(__name__)


db = get_db()


@app.route("/")
def hello_world():
    return 'The API is working'

#! Journals
@app.route("/journals")
def journals():
    journals = db.collection("journals").get()
    journals_list = []

    for journal in journals:
        journals_list.append(journal.to_dict())
    return jsonify(journals_list)


#! Articles
@app.route("/articles")
def articles():
    articles = db.collection("articles").get()
    articles_list = []

    for article in articles:
        articles_list.append(article.to_dict())
    return jsonify(articles_list)   


#! Issues
@app.route("/issues")
def issues():
    issues = db.collection("issues").get()
    issues_list = []

    for issue in issues:
        issues_list.append(issue.to_dict())
    return jsonify(issues_list) 


#! Volumes
@app.route("/volumes")
def volumes():
    volumes = db.collection("volumes").get()
    volumes_list = []   

    for volume in volumes:
        volumes_list.append(volume.to_dict())
    return jsonify(volumes_list)    


#! Current Articles of Active Volume in Active Issue with Journal Id
@app.route("/current-articles/<string:journal_id>")
def current_articles(journal_id):
    # Get the active volume
    volumes = db.collection("volumes").where("journalId", "==", journal_id).get()
    active_volume = None
    for volume in volumes:
        if volume.to_dict()["isActive"]:
            active_volume = volume.to_dict()
            break

    # Get the active issue
    issues = db.collection("issues").where("volumeId", "==", active_volume["id"]).get()
    active_issue = None
    for issue in issues:
        if issue.to_dict()["isActive"]:
            active_issue = issue.to_dict()
            break

    # Get the current articles
    current_articles = db.collection("articles").where("journalId", "==", journal_id).where("issueId", "==", active_issue["id"]).get()
    current_articles_list = []

    for article in current_articles:
        current_articles_list.append(article.to_dict())
    return jsonify(current_articles_list)


#! Current Issue of Active Volume with Journal Id
@app.route("/current-issues/<string:journal_id>")
def current_issue(journal_id):
    volumes = db.collection("volumes").where("journalId", "==", journal_id).get()
    active_volume = None
    for volume in volumes:
        if volume.to_dict()["isActive"]:
            active_volume = volume.to_dict()
            break

    issues = db.collection("issues").where("volumeId", "==", active_volume["id"]).get()
    active_issue = None
    for issue in issues:
        if issue.to_dict()["isActive"]:
            active_issue = issue.to_dict()
            break
    return jsonify(active_issue)


#! Volume of Journal with Journal Id
@app.route("/volumes/<string:journal_id>")
def volume_by_journal(journal_id):
    volumes = db.collection("volumes").where("journalId", "==", journal_id).get()
    volumes_list = []
    for volume in volumes:
        volumes_list.append(volume.to_dict())
    return jsonify(volumes_list)

#! Issue of Volume with Volume Id
@app.route("/issues/<string:volume_id>")
def issue_by_volume(volume_id):   
    issues = db.collection("issues").where("volumeId", "==", volume_id).get()
    issues_list = []
    for issue in issues:
        issues_list.append(issue.to_dict())
    return jsonify(issues_list)

#! Articles of Issue with Issue Id
@app.route("/articles/<string:issue_id>")
def articles_by_issue(issue_id):
    articles = db.collection("articles").where("issueId", "==", issue_id).get()
    articles_list = []
    for article in articles:
        articles_list.append(article.to_dict())
    return jsonify(articles_list)

if __name__ == "__main__":
    app.run(debug=True)
