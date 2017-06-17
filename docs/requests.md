
Create a user
---


```bash
curl -d '{"email":"johhny.doe@gmail.com","password":"passpass","picture":"pic"}' -H 'Content-type: application/json' localhost:5000/api/v1/users
```

Retrieve a user
---

```bash
curl localhost:5000/api/v1/users/1  
```


