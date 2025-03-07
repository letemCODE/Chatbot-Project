from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper
app = FastAPI()

inprogress_orders = {}

@app.post("/")

async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult'].get('outputContexts', [])
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])
    query_text = payload['queryResult']['queryText']
    print(query_text)
    intent_handler_dict = {
        'order.add - context: ongoing-order' : add_to_order,
        'order.remove - context: ongoing-order' : remove_from_order,
        'order.complete - context: ongoing-order' : complete_order,
        'track.order - context: ongoing-tracking' : track_order,
        'new.order' : new_order
    }
    return intent_handler_dict[intent](parameters, session_id)

def new_order(parameters: dict, session_id: str):
    if session_id in inprogress_orders: #when new order is entered the food-items are deleted but ses_id remains
        inprogress_orders[session_id] = {}

def add_to_order(parameters: dict, session_id: str) :
    food_items = parameters['food-item']
    quantities = parameters['number']
    if len(food_items) != len(quantities) :
        fulfillment_text = f"Sorry I didn't understand that. Can you please specify the Food Items and the Quantity"
    else:
        new_food_dict = dict(zip(food_items, quantities))
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict
        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have {order_str}. Would you like anything else?"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

def complete_order(parameter: dict, session_id: str) :
    if session_id not in inprogress_orders :
        fulfillment_text = f"I'm having trouble finding your order. Sorry! Please place a New Order."
    else:
        order = inprogress_orders[session_id] #gets food dict
        order_id = save_to_db(order)
        # print("**************")
        # print(inprogress_orders)
        if order_id == -1:
            fulfillment_text = (f"Sorry I could not place your order dur to a Backend Error. "
                                f"Please place a new order")
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = (f"Awesome! We have place your order ! "
                                f"Here is your Order ID {order_id} "
                                f"Your Order Total is £ {order_total}")
        # to remove the order
        del inprogress_orders[session_id]
        return JSONResponse(content={"fulfillmentText": fulfillment_text})

def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()
    for food_items, quantity in order.items():
        #check return code
        rcode = db_helper.insert_order_item(food_items, quantity, next_order_id)
        if rcode == -1:
            return -1
    #to update the progress of the order in the status table
    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id

def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={"fulfillmentText": "I'm having trouble finding your order. Sorry! Can you place a new order."})
    current_order = inprogress_orders[session_id]
    food_item = parameters["food-item"]
    quantities = parameters['number']
    remove_dict = dict(zip(food_item, quantities))
    removed_items = []
    no_such_items = []
    for item in food_item:
        if item not in current_order:
            no_such_items.append(item) #items that have not been ordered but been asked to remove
    #if only remove item is mentioned
    if len(quantities) == 0:
        for item in food_item:
            if item in current_order:
                removed_items.append(item) #keep track of removed items and quantity
                del current_order[item]
    #if remove item and quantity is mentioned
    elif ((len(quantities)) !=0) & (len(quantities) == len(food_item)):
        for item in food_item:
            if item in current_order:

                # if quantity of items to remove is <= quantity of items ordered
                if current_order[item] - remove_dict[item] > 0:
                    current_order[item] = current_order[item] - remove_dict[item]
                    remove_str = generic_helper.get_str_from_food_dict(remove_dict)
                    fulfillment_text = f'{remove_str} has been removed from your order.'

                # if quantity of items to remove is > quantity of items ordered
                else :
                    fulfillment_text = (f'Please specify the right quantity of items to remove or '
                                        f'just enter name of the item to remove all units of item ordered. ')

    #if quantity of items to remove is mentioned for one item but not for all
    else:
        fulfillment_text = (f'Please specify the quantity of items to remove or just enter name of the item '
                            f'to remove all units of item ordered. ')

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {" ,".join(removed_items)} from your order.'
    if len(no_such_items) > 0:
        fulfillment_text = f'Your current order does not have {" ,".join(no_such_items)}'
    if len(current_order.keys()) == 0:
        fulfillment_text += f'Your order is empty'
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Here is what is left in your order {order_str}"
    return JSONResponse(content={"fulfillmentText": fulfillment_text})

def track_order(parameters: dict, session_id: str) :
    order_id = int(parameters['order_id']) # to get the order id from diagnostic info -> fulfilment request
    # now we call sql db
    order_status = db_helper.get_order_status(order_id)
    if order_status :
        fulfillment_text = f"The order status for {order_id} is {order_status}"
    else :
        fulfillment_text = f"No order found with {order_id}"
    return JSONResponse(content={"fulfillmentText": fulfillment_text})