# Wordpress to Hugo

This script is used to export content from Wordpress to [Hugo](http://gohugo.io/).

# Usage

The requirements of this script is put in `requirements.txt`, the following steps show how to build the environment in `virtualenv`.

```
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
$ pip install  -r requirements.txt
```

After the installation done, the script can be executed via:

```
$ ./wp2hugo.py wordpress.xml
```

The `wordpress.xml` used here is exported from Wordpress export tool.

All exported things will be saved into `./hugo` directory. The meta data will be saved into `./hugo/config.yaml` file, while the public posts will be converted to markdown files with [front matter](http://gohugo.io/content/front-matter/) info, and saved in `./hugo/posts/` directory.

