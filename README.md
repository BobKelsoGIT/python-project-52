<h2 align="center">Task Manager</h2>
<h3 align="center">Allows creating tasks, assigning them to a performer, setting labels, and status.</h3>
<hr>

### Tests and linter status:
[![Actions Status](https://github.com/BobKelsoGIT/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/BobKelsoGIT/python-project-52/actions)
[![Actions Status](https://github.com/BobKelsoGIT/python-project-52/actions/workflows/check.yml/badge.svg)](https://github.com/BobKelsoGIT/python-project-52/actions)
### Maintainability and test coverage:
[![Maintainability](https://api.codeclimate.com/v1/badges/81c87d1f0f6848f108ee/maintainability)](https://codeclimate.com/github/BobKelsoGIT/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/81c87d1f0f6848f108ee/test_coverage)](https://codeclimate.com/github/BobKelsoGIT/python-project-52/test_coverage)

<h2>You can see the  <a href='https://task-manager-k0d2.onrender.com'>example here.</a></h2>

<table>
   <tr> 
    <td><h3>Requirements:</h3></td><td><h3>Installation instructions:</h3></td>
   </tr>
    <tr>
        <td> Python = > 3.10
            </td>
        <td>

```Python
# command
git clone https://github.com/BobKelsoGIT/python-project-52.git

# command
poetry install

# Create ".env" file in the root directory with next parameters:
    SECRET_KEY=
    DEBUG=
    DATABASE_URL=
    ACCESS_TOKEN= #If you use error tracking with Rollbar.
    
# command
poetry run python manage.py migrate

#!For develop: command
make dev

#!For production: command
make start
```

</td>
</tr>
  </table>

<hr>
