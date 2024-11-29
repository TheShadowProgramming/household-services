<h1 class="text-center text-primary lato-black">Closed Service Requests</h1>
    <div class="container lato-regular border border-5 border-primary text-center">
        <div class="row">
            <div style="font-size: 1.25rem;" class="col-4 text-white lato-bold bg-primary">DB Id</div>
            <div style="font-size: 1.25rem;" class="col-4 text-white lato-bold bg-primary">Negotiated Price</div>
            <div style="font-size: 1.25rem;" class="col-4 text-white lato-bold bg-primary">Pincode</div>
        </div>
            {% for tuple in service_requests_closed %}
                <div style="border-bottom: 0.5px solid;" class="row border-secondary">
                    <div style="background-color: hsla(0, 0%, 66%, 0.251);" class="col-4 text-black border-1 border-start border-end border-secondary d-flex align-items-center justify-content-center">{{ tuple.service_id }}</div>
                    <div class="col-4 d-flex align-items-center justify-content-center">{{ tuple.service_price }}</div>
                    <div class="col-4 d-flex align-items-center justify-content-center">{{ tuple.customer_pincode }}</div>
                </div>            
            {% endfor %}
    </div>

- we'll see why is this not working