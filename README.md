<p align="center">
<a href="https://dscvit.com">
	<img width="400" src="https://user-images.githubusercontent.com/56252312/159312411-58410727-3933-4224-b43e-4e9b627838a3.png#gh-light-mode-only" alt="GDSC VIT"/>
</a>
	<h2 align="center"> < Insert Project Title Here > </h2>
	<h4 align="center"> < Insert Project Description Here > <h4>
</p>

---
[![Join Us](https://img.shields.io/badge/Join%20Us-Developer%20Student%20Clubs-red)](https://dsc.community.dev/vellore-institute-of-technology/)
[![Discord Chat](https://img.shields.io/discord/760928671698649098.svg)](https://discord.gg/498KVdSKWR)

[![DOCS](https://img.shields.io/badge/Documentation-see%20docs-green?style=flat-square&logo=appveyor)](INSERT_LINK_FOR_DOCS_HERE) 
  [![UI ](https://img.shields.io/badge/User%20Interface-Link%20to%20UI-orange?style=flat-square&logo=appveyor)](INSERT_UI_LINK_HERE)

## ML API Features
<h5>1. Request: GET /get_question/cnt </h5> 
- Desc: to get recommendations<br>
- Parameter: cnt (integer >=0) to recommend questions from the next cluster of lowest probability <br>
- Response: {
                "id":<value>, 
                "title": <value>, 
                "difficulty": <value>, 
                "related_topics": <value>
            }<br>
  
<h5> 2. Request: GET /retrain </h5>
- Desc: to retrain the model <br>
- Response: {
                "retrain_model": "success", 
                "message": "Model has been updated"
            }<br>
  
<h5>3. Request: POST /data_process_task/ </h5>
- Desc: to update datasets with new input data <br>
- Input: {
              "user_id": 123, 
              "question_id": 123,  
              "time_taken": 120, 
              "liked": true
          }<br>
- Response: {
                "title": <value>, 
                "difficulty": <value>, 
                "related_topics": <value>, 
            }<br>




## Dependencies
- **Python**: `>=3.9.10`
- **scipy**: `>=1.11.0`
- **scikit-learn**: `=1.3.2`
- **numpy**: `>=1.25`
- **pandas**: `>=2.0.3`
- **flask**: `>=3.0.0`
- **joblib**: `>=1.3.1`
<br>

## Running

Install the other required dependencies using the following command, given that python is installed:

```bash
pip install -r requirements.txt
```
Navigate to the project directory. Now, you can run the development server using the command:<br>
```bash
flask --app mlapi run
```
You can test the API using cURL with the following commands:<br>
GET Request,
```bash
curl "http://example.com/get_question/<int>"
```
```bash
curl "http://example.com/retrain"
```
POST Request
```bash
curl -H "Content-Type: application/json" -d "{\"example\":123}" "http://example.com/data_process_task"
```
<br>
Or you can use Postman API. Learn more about it at https://learning.postman.com/docs/designing-and-developing-your-api/deploying-an-api/deploying-an-api-overview/
<br>


## Contributors

<table>
	<tr align="center">
		<td>
		John Doe
		<p align="center">
			<img src = "https://dscvit.com/images/dsc-logo-square.svg" width="150" height="150" alt="Your Name Here (Insert Your Image Link In Src">
		</p>
			<p align="center">
				<a href = "https://github.com/person1">
					<img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36" alt="GitHub"/>
				</a>
				<a href = "https://www.linkedin.com/in/person1">
					<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36" alt="LinkedIn"/>
				</a>
			</p>
		</td>
	</tr>
</table>

<p align="center">
	Made with ❤ by <a href="https://dscvit.com">GDSC-VIT</a>
</p>
