<!-- Logistic -->

BASE URL: "http://localhost:5000"

<!-- Seller Range Details -->

<!-- Adding Details -->

URL: "/api/seller"
METHOD: POST
BODY: {
    rating: Float,
    ran: String
}
RESPONSE: "Data Inserted", 200 OK

<!-- Getting Details -->

URL: "/api/seller"
METHOD: GET
RESPONSE: Array Of JSON Object, 200 OK

<!-- Buyer Data (PIN and LEVEL) -->

<!-- Adding Data -->

URL: "/api/buyerdata"
METHOD: POST
BODY: {
    pin: Integer,
    level: Integer
}
RESPONSE: "Inserted Data", 200 OK

<!-- Getting Data -->

URL: "/api/buyerdata"
METHOD: GET
RESPONSE: Array Of JSON Object, 200 OK

<!-- Seller Data (PIN and LEVEL) -->

<!-- Adding Data -->

URL: "/api/sellerdata"
METHOD: POST
BODY: {
    pin: Integer,
    level: Integer
}
RESPONSE: "Inserted Data", 200 OK

<!-- Getting Data -->

URL: "/api/sellerdata"
METHOD: GET
RESPONSE: Array Of JSON Object, 200 OK