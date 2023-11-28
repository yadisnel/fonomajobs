# fonomajobs
Fonoma - Backend Developer Test

## Steps

1. Create a FastAPI basic project following this tutorial: https://fastapi.tiangolo.com/tutorial/first-steps
   * Done, the project is created,  branch for the basic project is "main"
2. Create a git repository with the code and upload it to Github, Gitlab or Bitbucket:
   * Done: https://github.com/yadisnel/fonomajobs
3. In the repository, create a new branch:
   * Done, branch "develop" is created
4. In the new branch, implement a new endpoint with the path`/solution`. This endpoint should accept a POST request with the parameters of the coding exercise described in the section**[Coding exercise](https://www.notion.so/Fonoma-Backend-Developer-Test-2e5f72834bb44c2ea76b8e972332e9c1?pvs=21)** that is below. The endpoint should return the result of executing the function`process_orders`with the parameters obtained from the post.
    
* Real request with 'completed' filter:
```
   curl -X 'POST' \
  'https://fonomajobs.onrender.com/v1/solution' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
   "orders": [
       {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
       {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
       {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
       {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"}
   ],
   "criterion": "completed"
}'
}'
```
* Response: 
```
{
  "total": 1299.69
}
```
* Real request with 'all' filter:
```
   curl -X 'POST' \
  'https://fonomajobs.onrender.com/v1/solution' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
   "orders": [
       {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
       {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
       {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
       {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"}
   ],
   "criterion": "all"
}'
}'
```
* Response: 
```
{
  "total": 2399.55
}
```
* All parameters are validated.
5. Write at least one unit test for the /solution endpoint. More tests will give you bonus points:
* There are about 8 unit tests, not only for the endpoint:
```
collected 8 items                                                               

test_main.py ..                                                 [ 25%]
controllers/test_order                                          [ 50%]
routers/v1/test_orders                                          [100%]
======== 8 passed in 0.75s ===========
```
6. Created a Pull Request of the new branch with a detailed description of the changes made.
7. Deployed the application to[Render.com](http://render.com/). 
* https://fonomajobs.onrender.com/v1/docs#/orders/process_orders_solution_post
* Done: **Bonus points**: In step 4, use a docker image for the deployment. 
* Done: **Bonus points**: Use Redis to cache the results of the requests to`/solution`.
* Done: **Bonus points**: Add type annotations.

