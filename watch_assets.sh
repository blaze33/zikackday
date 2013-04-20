# Compile coffee to js
coffee -o static/js/ -cw front/coffee/ &

# Compile sass to css
sass --watch front/sass/zhd.sass:static/css/zhd.css &
