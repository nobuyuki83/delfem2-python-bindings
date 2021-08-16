curl --request POST 'https://api.github.com/repos/nobuyuki83/delfem2-python-bindings/dispatches' \
--header 'Authorization: Bearer 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' \
--header 'Content-Type: application/json' \
--data-raw '{
	"event_type": "updated-delfem2"
}'