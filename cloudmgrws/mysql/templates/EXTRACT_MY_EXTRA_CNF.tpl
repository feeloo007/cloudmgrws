cat << EOF
{ "version":
    $( {% include 'GET_MYSQL_VERSION.tpl' %} )
,
"content":
    [
        $( {% include 'GET_CONTENT_MY_EXTRA_CNF.tpl' %} )
    ]
}
EOF
