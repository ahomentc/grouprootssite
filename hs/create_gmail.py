from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
import time
import re

class GmailBot():
    def __init__(self, username, password, name1, name2):
        self.browserProfile = webdriver.ChromeOptions()
        # self.browserProfile.add_argument('headless')
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.browserProfile)
        self.username = username
        self.password = password
        self.name1 = name1
        self.name2 = name2
        self.contacted = set()
        self.formatted_to_contact = []
        self.numberSent = 0

    def signUp(self):
        self.browser.get('https://accounts.google.com/signup/v2/webcreateaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ltmpl=default&dsh=S-133663510%3A1608186447801931&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp')

        time.sleep(5)
        name1Input = self.browser.find_elements_by_css_selector('form input')[0]
        name2Input = self.browser.find_elements_by_css_selector('form input')[1]
        usernameInput = self.browser.find_elements_by_css_selector('form input')[2]
        password1Input = self.browser.find_elements_by_css_selector('form input')[3]
        password2Input = self.browser.find_elements_by_css_selector('form input')[4]

        name1Input.send_keys(self.name1)
        name2Input.send_keys(self.name2)
        usernameInput.send_keys(self.username)
        password1Input.send_keys(self.password)
        password2Input.send_keys(self.password)
        password2Input.send_keys(Keys.ENTER)
        time.sleep(5)

    def finishSignUp(self):
        # select_month = Select(self.browser.find_element_by_id("month"))
        # select_month.select_by_index(0)

        dayInput = self.browser.find_element_by_id("day")
        dayInput.send_keys("16")

        yearInput = self.browser.find_element_by_id("year")
        yearInput.send_keys("1997")

        # select_gender = Select(self.browser.find_element_by_id("gender"))
        # select_gender.select_by_index(0)

        submit_buttom = self.browser.find_element_by_class_name("VfPpkd.RLmnJb")
        submit_buttom.click()

        time.sleep(5)
        
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        terms_button = self.browser.find_element_by_class_name("RveJvd.snByac")
        terms_button.click()

    def sendDms(self):
        self.browser.get('https://www.instagram.com/direct/inbox/')
        time.sleep(2)

        notificationButton = self.browser.find_element_by_class_name('aOOlW.HoLwm')
        notificationButton.click()
        time.sleep(2)

        for user in self.formatted_to_contact:
            username = user[0]
            name = user[1]

            if self.numberSent > 30:
                print("Sent to 30 users. Done for the day.")
                break

            if username in self.contacted:
                continue

            try:
                composeButton = self.browser.find_element_by_class_name('wpO6b.ZQScA')
                composeButton.click()
                time.sleep(5)

                toInput = self.browser.find_element_by_class_name('j_2Hd.uMkC7.M5V28')
                toInput.send_keys(username)
                time.sleep(5)

                selectButton = self.browser.find_element_by_class_name('dCJp8')
                selectButton.click()
                time.sleep(5)
                
                nextButton = self.browser.find_element_by_class_name('sqdOP.yWX7d.y3zKF.cB_4K')
                nextButton.click()
                time.sleep(5)

                # Make it be: Hi [name or username if name is empty ]!
                messageInput = self.browser.find_element_by_css_selector('textarea')

                if name == "":
                    messageInput.send_keys("Hi " + username + "! We’re launching a new social app based on group profiles (kinda like those accounts people make on Instagram for their friend groups)")
                else:
                    messageInput.send_keys("Hi " + name + "! We’re launching a new social app based on group profiles (kinda like those accounts people make on Instagram for their friend groups)")
                messageInput.send_keys(Keys.SHIFT + Keys.ENTER)
                messageInput.send_keys(Keys.SHIFT + Keys.ENTER)
                messageInput.send_keys("The idea is to show your followers what friend groups you’re in and what the groups are like. Would you be able to check out our profile and let us know what you think?")
                messageInput.send_keys(Keys.SHIFT + Keys.ENTER)
                messageInput.send_keys(Keys.SHIFT + Keys.ENTER)
                messageInput.send_keys("We want our app to be based on what people like. So it’s important for us to get feedback from people that matter. People we’ve been talking with so far seem really excited about it.")
                messageInput.send_keys(Keys.SHIFT + Keys.ENTER)
                messageInput.send_keys(Keys.SHIFT + Keys.ENTER)
                messageInput.send_keys("You can just respond here with your thoughts if you have the time.")
                messageInput.send_keys(Keys.SHIFT + Keys.ENTER)
                messageInput.send_keys(Keys.SHIFT + Keys.ENTER)
                messageInput.send_keys("Thanks!")
                time.sleep(5)
                
                # find the send button
                buttons = self.browser.find_elements_by_css_selector('button')
                for button in buttons:
                    if button.text == 'Send':
                        button.click()
                        self.numberSent += 1
                        break

                # pop from formatted_to_contact
                self.formatted_to_contact.pop(0)

                # save formatted_to_contact to file
                with open('people_to_contact.txt', 'w') as f: # this is a replace operation
                    for formatted_user in self.formatted_to_contact:
                        f.write(formatted_user[0] + "|" + formatted_user[1] + "\n")

                # add username to contacted.txt
                with open('contacted.txt', 'a') as f: # this is an append operation
                    f.write(username + "\n")

                time.sleep(900)

            except:
                # pop from formatted_to_contact
                self.formatted_to_contact.pop(0)

                # save formatted_to_contact to file
                with open('people_to_contact.txt', 'w') as f: # this is a replace operation
                    for formatted_user in self.formatted_to_contact:
                        f.write(formatted_user[0] + "|" + formatted_user[1] + "\n")

                # add username to contacted.txt
                with open('contacted.txt', 'a') as f: # this is an append operation
                    f.write(username + "\n")

                self.browser.get('https://www.instagram.com/direct/inbox/')
                time.sleep(5)

    def getUserFollowers(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
    
        followersList.click()
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)
        
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        return followers

    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()

if __name__ == "__main__":
    
    with open("high_school_cali_emails_2.txt") as f:
        usernames = [line.split('@')[0] for line in f.readlines()]
        for username in usernames:
            bot = GmailBot(username, 'InstaGroupRoots8', username, 'app')
            bot.signUp()
            input("Press Enter to continue...")
            bot.finishSignUp()
            time.sleep(5)

            input("Press Enter to continue...")
    
    # bot = GmailBot('sf_grouproots', 'Andrei162693', '', 'app')
    # bot.signup()
    # time.sleep(5)

    # with open('people_to_contact.txt') as f:
    #     to_contact = [username.rstrip() for username in f.readlines()]
    #     for contact in to_contact:
    #         if "|" in contact:
    #             username = contact.split('|')[0]
    #             name = contact.split('|')[1]
    #             if len(name.split()) > 0:
    #                 name = name.split()[0]
    #             name = re.sub(r'\W+', '', name)
    #             name = name.capitalize()
    #             # need to format name to remove all symbols, capitalize it, and only keep first name
    #             # only user name if its not ""
    #             bot.formatted_to_contact.append(tuple([username,name]))
    #         else:
    #             bot.formatted_to_contact.append(tuple([contact,""]))

    # with open('contacted.txt') as f:
    #     bot.contacted = set([username.rstrip() for username in f.readlines()])
            
    # bot.sendDms()






























