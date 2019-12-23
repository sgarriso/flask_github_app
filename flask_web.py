from flask import Flask ,render_template,abort
import sqllite_helper
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')
@app.route('/list')
def list_view():
    #{% if Record_list %}
#	<p>  top 50 Python Github repos:</p>
 #   <ul>
  #  {% for Record in Record_list %}
   #     <li><a href="{% url 'github_display_app:record_detail'  Record.repository_ID %}">{{ Record.name }}</a></li>
   # {% endfor %}
   # </ul>
#{% else %}
#    <p>No Records are available.</p>
#{% endif %}
    conn = sqllite_helper.setup()
    values = sqllite_helper.get_values(conn)
    conn.close()
    output = ""
    if values:
        output = output + '<p>  top 50 Python Github repos:</p><ul>'
        for value in values[0:50]:
            output = output + '<li><a href="/list/record/' + value['repository_ID'] +  '/">' + value['name']+ '</a></li>'
        output = output + '</ul>'
    else:
        output = '<p>No Records are available.</p>'
    print(output)
    return output
@app.route('/list/record/<repo_id>/')
def detail_view(repo_id):
    conn = sqllite_helper.setup()
    values = sqllite_helper.get_values_by_id(conn,repo_id)
    conn.close()
    output = ""
    print(values)
    if not values:
        abort(404)
    #{% for f in record.get_printable_fields %}
  #<dt>{{f.label|capfirst}}</dt>
   # <dd>
    #  {{f.value|escape|urlize|linebreaks}}
    #</dd>
#{% endfor %}
    for key in values.keys():
        if key != 'id':
            output  = output + '<dt>' + str(key) + '</dt><dd>' + str(values[key]) + '</dd>'
    return output
    

if __name__ == '__main__':
    app.run()

