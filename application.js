var request = require('request');
var cookieJar = request.jar();
var BrowserWindow = require('electron').remote.BrowserWindow;
var remote = require('electron').remote;


function hide_view(view_id) {
    let view = document.getElementById(view_id);
    view.className += ' hidden';
}

function set_view(view_id) {
    let view = document.getElementById(view_id);
    let views = document.querySelectorAll('.view');
    for(var ii = 0; ii < views.length; ii++) {
        let v = views[ii];
        if (v == view) { continue; }

        if (v.className.indexOf(' hidden') == -1) {
            v.className += ' hidden';
        }
    }
    view.className = view.className.replace(' hidden', '');
}

function login(_email, _password, callback) {

    request.post(
            'http://127.0.0.1:5000/login',
            { form: { email: _email, password: _password, jar: cookieJar} },
            function (error, response, body) {
                if (!error && response.statusCode == 200) {
                    callback(JSON.parse(body));
                }
            }
            );
}

function get_user(_user_id, callback) {
    var url = 'http://127.0.0.1:5000/user/'+_user_id
    if (_user_id == null || _user_id == undefined) {
        url = 'http://127.0.0.1:5000/user';
    }

    console.log(url);

    request.get(
            url,
            {jar: cookieJar},
            function (error, response, body) {
                if (!error && response.statusCode == 200) {
                    callback(JSON.parse(body));
                }
            }
            );
}

function register(_firstname, _lastname, _email, _password, callback) {

    request.post(
            'http://127.0.0.1:5000/register',
            {
                form: {
                    firstname: _firstname,
                    lastname: _lastname,
                    email: _email,
                    password: _password,
                    jar: cookieJar
                }
            },
            function (error, response, body) {
                if (!error && response.statusCode == 200) {
                    callback(JSON.parse(body));
                }
            }
            );
}

function update_userinfo(user) {
    document.getElementById('firstname').innerHTML = user.firstname;
    document.getElementById('user-id').value = user.user_id;
}

function update_contacts(contacts) {
    let contact_list = document.getElementById('contact-list');
    for (var i = 0; i < contacts.length; i++) {
        get_user(contacts[i], function(contact_user) {
            var item = document.createElement('div');
            item.className = 'item';
            var img = document.createElement('img');
            img.className = 'contact-icon';
            img.setAttribute('src', 'static/image/msn_icon.png');
            var p = document.createElement('p');
            p.innerHTML = contact_user.firstname;
            var span = document.createElement('span');
            span.innerHTML = 'test';

            item.appendChild(img);
            item.appendChild(p);
            item.appendChild(span);

            item.setAttribute('user-id', contact_user.user_id);

            item.addEventListener('click', function(e) {
                remote.getGlobal('clicked_contact').user_id = this.getAttribute('user-id');
                win = new BrowserWindow({width: 740, height: 512});
                win.loadURL(`file://${__dirname}/chat.html`);
            });

            contact_list.appendChild(item);

        });
    }
}

console.log(cookieJar);
