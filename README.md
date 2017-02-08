avispa
======

Tool to manually capture data into a local ring


"get_a" = Show all the rings of user <a>
"get_a_b" = Show all the items of ring <a>/<b>
"get_a_b_c" = Show item <a>/<b>/<c>
"get_a_x" = Show all collections from user <a>
"get_a_x_y" = Show collection <y> from user <a>
"get_a_x_y_b" = Show ring <a>/<b> as part of collection <y>
"get_a_x_y_b_c" = Show item <a>/<b>/<c> as part of collection <y>
"post_a" = Create new ring for user <a>
"post_a_b" = Create new item in ring <a>/<b>
"post_a_x" = Create new collection for user <a>
"put_a" = Update user <a>
"put_a_b" = Update ring <a>/<b>
"put_a_b_c" = Update item <a>/<b>/<c>
"put_a_x_y" = Update collection <y> from user <a>
"delete_a" = Delete user <a>
"delete_a_b" = Delete ring <a>/<b>
"delete_a_b_c" = Delete item <a>/<b>/<c>
"delete_a_x_y" = Delete collection <y> from user <a>



## Dev machine setup

1. Clone repository

2. Place env_config.py (development version) in the root. 
   ***This config file is not included in the repository ***

3. from the project root, run :
```
$ source life/app_dependencies_dev.sh
```

4. Run the dev flask version 
```
$ python run.sh
```

















