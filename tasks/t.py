if __name__ == '__main__':
    sean = {
               "first_name": "sean",
               "last_name": "lew",
               "city": "los angeles"
           },
    asa = {
              "first_name": "asa",
              "last_name": "butterfield",
              "city": "london",
          },
    freddie = {
                  "first_name": "freddie",
                  "last_name": "fox",
                  "city": "london"
              },
    peoples = [sean, asa, freddie]
    for people in peoples:
        for username, user_info in people.items():
            print("\nUsername is: " + username)
        full_name = (people["first_name"] + " " + people["last_name"])
        city = (people["city"])

        print("\tFull name is : " + full_name.title() + ".")
        print("\tCity is : " + city.title() + ".")
