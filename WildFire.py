import time
import random

#Person class
class Person:
    #Attributes of a Person class: name, age, gender, environment, size, weather, and acre_input
    def __init__(self, name, age, gender, environment, size, weather, acre_input=None): 
        self.name = name
        self.age = age
        self.gender = gender
        self.environment = environment
        self.size = size
        self.weather = weather
        self.acre_input = acre_input

    #String representation of the Person class
    def __str__(self):
      return ( 
          f"Wildfire reported by {self.name}\n"
          f"Name: {self.name}\n"
          f"Age: {self.age}\n"
          f"Gender: {self.gender}\n"
          f"Environment: {self.environment}\n"
          f"Size: {self.size}\n"
          f"Weather: {self.weather}  \n"
      )

#PersonReport function (essentially a constructor for the Person class)
def PersonReport():
    #Valid inputs for weather and environment
    valid_weather = ['Windy', 'Sunny', 'Rainy', 'Snowy']
    valid_environment = ['Dense Forest', 'Grass Fields', 'Rural Area']

    print('--- Person Report ---')

    #Input for name, age, and gender of the person reporting the wildfire
    name = input('Enter your name: ')
    age = input('Enter your age: ')
    gender = input('Enter your gender: ')

    #This loop ensures that the user inputs a valid number for the fire size, it also has an exception error for invalid inputs
    while True:
      try:
          size_input = input("Enter approximate fire size (example: '0.5 acre' or '2 acres'): ").lower()
          acre_value = float(size_input.split()[0])
          #Determines the size of the fire based on the inputted number with fires ranging from Small, Medium, to Large
          if acre_value < 1:
              size = 'Small'
          elif 1 <= acre_value <= 3:
              size = 'Medium'
          else:
              size = 'Large'
          break
      #Exception error for invalid inputs
      except(ValueError, IndexError):
          print("Please enter a valid number followed by 'acre' or 'acres' (example: '0.5 acre' or '2 acres').")

    #This loop ensures that the user inputs a valid weather condition
    while True:
        weather = input('Enter current weather (Windy, Sunny, Rainy, Snowy): ')
        if weather in valid_weather:
            break
        else:
            print("Please make sure capitalization is correct or weather inputted is valid.")

    
    #This loop ensures that the user inputs a valid environment
    while True:
        environment = input('Enter your environment (Dense Forest, Grass Fields, Rural Area): ')
        if environment in valid_environment:
            break
        else:
            print("Please make sure capitalization is correct or environment inputted is valid.")

    #Finally after all the inputs are valid, the Person class is returned with the user's inputs as the parameters
    return Person(name, age, gender, environment, size, weather, acre_input= size_input)

#WildFire class, inherits from the Person class
class WildFire(Person):
      #Environtment = 'Dense Forest', 'Grass Fields', 'Rural Area'
      #Size = 'Large', 'Medium', 'Small'
      #Weather = 'Windy', 'Sunny', 'Rainy'

      #Attributes of the WildFire class: name, age, gender, environment, size, weather, and acre_input
      def __init__(self, name, age, gender, environment, size, weather, acre_input):
        #Inherits the attributes from the Person class
        super().__init__(name, age, gender, environment, size, weather, acre_input)
        self.firePercentage = 100
        self.numDispatchers = self.initialDispatchers()
        self.totalDispatchers = self.numDispatchers
        self.minutes = 0
        self.areaBurned = 0

      #Determines the initial number of dispatchers based on the severity of the fire
      def initialDispatchers(self):
        #Severity of the fire is determined by the environment, size, and weather using the calcSeverity function
        severity = self.calcSeverity()
        #Based on the severity, the number of dispatchers is determined
        if severity >= 8:
          return 10
        elif severity >= 5:
          return 7
        else:
          return 4

      #Calculates the severity of the fire based on the environment, size, and weather
      def calcSeverity(self):
        #As the user inputs the environment, size, and weather, the severity is determined by the following dictionaries
        environment = {'Dense Forest': 3, 'Grass Fields': 2, 'Rural Area': 1}
        size = {'Large': 3, 'Medium': 2, 'Small': 1}
        weather = {'Windy': 3, 'Sunny': 2, 'Rainy': 1, 'Snowy': 0.5}
        #Returns a number that represents the severity of the fire according to the user's inputs
        return environment[self.environment] + size[self.size] + weather[self.weather]

      #Simulation of the wildfire, calls the recursive function _simRecursive
      def simulation(self):
        self._simRecursive(previous_fire=self.firePercentage)

      #Recursive function that simulates the wildfire, it ends when the firePercentage is less than or equal to 0, basically when the fire is out
      def _simRecursive(self, previous_fire):
        if self.firePercentage <= 0:
            self.Report()
            return

        #Calculates the severity of the fire, the suppression, and the growth of the fire
        severity = self.calcSeverity()
        #Suppresion is calculated by the number of dispatchers and a random number between 1.5 and 3.0
        suppression = self.numDispatchers * random.uniform(1.5, 3.0)
        #Growth is calculated by the severity and a random number between 0.5 and 1.2
        growth = severity * random.uniform(0.5, 1.2)

        #Calculates the new firePercentage by subtracting the suppression and adding the growth to the previous firePercentage
        new_fire = max(0, self.firePercentage - suppression + growth)
        #Drop is the difference between the previous firePercentage and the new firePercentage
        drop = self.firePercentage - new_fire
        self.firePercentage = new_fire
        #Burn rate is calculated by the severity and a random number between 0.1 and 0.4
        burn_rate = severity * random.uniform(0.1, 0.4)
        self.areaBurned += burn_rate
        #Keeping track of the time
        self.minutes += 1

        #If the drop is greater than or equal to 15, the minutes added in a random number between 1 and 4
        if drop >= 15:
          minutes_added = random.randint(1, 4)
        #else if the drop is less than 15 then more dispatchers are sent and the minutes added is a random number between 2 and 6
        else:
          minutes_added = random.randint(2, 6)
          self.numDispatchers += 1
          self.totalDispatchers += 1
          print(f"Fire not decreasing fast enough. Sending more dispatchers: {self.numDispatchers}")

        #Tracks the total time it takes to put out the fire
        self.minutes += minutes_added

        #Printing out time, firePercentage, and number of dispatchers as it goes through the simulation
        print(f"Time: {self.minutes} min | Fire: {self.firePercentage:.2f}% | Dispatchers: {self.numDispatchers}")
        time.sleep(0.5)
        #Recursive call
        self._simRecursive(previous_fire=self.firePercentage)

      #Report function that prints out the final report of the wildfire, as well as the time it took to put out the fire
      def Report(self):
        hours = self.minutes // 60
        minutes = self.minutes % 60
        total_burnt = self.areaBurned + float(self.acre_input.split()[0])
        print("\nFinal Report")
        print(f"Reported by: {self.name}, Age: {self.age}, Gender: {self.gender}")
        print(f"Environment: {self.environment}, Size: {self.acre_input}, Weather: {self.weather}")
        print(f"Time Taken: {hours}h {minutes}min")
        print(f"Dispatchers at Start: {self.numDispatchers - (self.numDispatchers - self.initialDispatchers())}")
        print(f"Dispatchers at End: {self.numDispatchers}")
        print(f"Total Area Burned: {total_burnt:.2f} acres")

#Main function
if __name__ == "__main__":

  print("Welcome to the Wildfire Reporting System!")
  #This loop ensures that the user can report multiple wildfires
  while True:
      #Person PersonPerport object is created and the user's inputs are stored in the object
      person = PersonReport()
      print(f'Thank you {person.name}, dispatchers are on their way!')
      #WildFire object is created and the user's from the Person object are stored in the WildFire object
      wildfire = WildFire(
          person.name,
          person.age,
          person.gender,
          person.environment,
          person.size,
          person.weather,
          person.acre_input
      )
      #Prints out the wildfire report
      print(f"Wildfire reported by {person.name} in a {person.environment} with a size of {person.acre_input} and {person.weather} weather.")
      
      #Simulation of the wildfire
      wildfire.simulation()

      #Asks the user if they want to report another wildfire, if anything other than 'yes' is inputted, the loop breaks and the program ends
      again = input("\nWould you like to report another fire? (yes/no): ").strip().lower()
      if again != 'yes':
          print("Thank you for using the Wildfire Reporting System!")
          break
  
      
    




wildfire_test = WildFire('TestUser', 30, 'Female', 'Grass Fields', 'Medium', 'Windy', '2 acres')

# Call calcSeverity and print it
severity = wildfire_test.calcSeverity()
print(f"Test Wildfire Severity: {severity}")