from django.http import HttpResponse

def message(request):
    message = "Happy Birthday Laurence<p>"
    
    message = message + "<a href = http://jeanflower.pythonanywhere.com/laurence/messages>click here for a longer message!</a><p>"
    url = 'http://jeanflower.pythonanywhere.com/laurence/codes/hello/0'
    message = message + "Or go to <a href = '"+url+"'>"+url+"</a><p>"
    message = message + "Try things other than hello and 0."
    message = message + "<p><p>"
    url = 'http://pythonfiddle.com/'
    message = message + "To play with the code, go to <a href = '"+url+"'>"+url+"</a><br>"
    message = message + "copy and paste in this code, hit \"run\":<br>"
    message = message + "<pre>\
def make_coded_message(uncoded_message, shift):<br>\
    # first set up an empty string to add characters to<br>\
    # this will become the coded message after we've added characters<br>\
    # one by one<br>\
    message_coded = \"\"<br>\
<br>\
    # look at each character of the uncoded message, one by one<br>\
    # use lowercase characters<br>\
    for character in uncoded_message.lower():<br>\
        if character == ' ':<br>\
            message_coded = message_coded + ' '<br>\
            continue<br>\
        # turn this character into a number; the natural translation is<br>\
        # a-> 97, b-> 98 and so on<br>\
        number_form =  ord(character)<br>\
        # alter the number so that a->0, b->1 and so on<br>\
        number_form = number_form - 97<br>\
        # alter the number to apply the code; add shift<br>\
        number_form = number_form + shift<br>\
        # if numbers became more than 25 (e.g. z would go to more)<br>\
        # wrap the numbers back using modulo arithmetic<br>\
        # now all our letters are between 0 and 25<br>\
        number_form = number_form % 26<br>\
        # finally, the computer wants to map 97->a, 98->b etc<br>\
        number_form = number_form + 97<br>\
        # convert the number back to a character and add it to the end<br>\
        # of the encoded message<br>\
        message_coded = message_coded + chr(number_form)<br>\
    return message_coded<br>\
<br>\
print(make_coded_message(\"happy birthday laurence\", 1))<br>\
    </pre>"
    message = message + "<p><p>"    
    message = message + "Have fun! Love from Jean and Gem."
    return HttpResponse(message)


def make_coded_message(uncoded_message, shift):
    # first set up an empty string to add characters to
    # this will become the coded message after we've added characters
    # one by one
    message_coded = ""

    # look at each character of the uncoded message, one by one
    # use lowercase characters
    for character in uncoded_message.lower():
        if character == ' ':
            message_coded = message_coded + ' '
            continue
        # turn this character into a number; the natural translation is
        # a-> 97, b-> 98 and so on
        number_form =  ord(character)
        # alter the number so that a->0, b-> 1 and so on
        number_form = number_form - 97
        # alter the number to apply the code; add shift
        number_form = number_form + shift
        # if numbers became more than 25 (e.g. z would go to more)
        # wrap the numbers back using modulo arithmetic
        # now all our letters are between 0 and 25
        number_form = number_form % 26
        # finally, the computer wants to map 97->a, 98->b etc
        number_form = number_form + 97
        # convert the number back to a character and add it to the end
        # of the encoded message
        message_coded = message_coded + chr(number_form)
    return message_coded

def codes(request, message, shift):
    return HttpResponse(make_coded_message(message, int(shift)))
    
def messages(request):
    message = "happy birthday laurence"
    response = "<pre>"
    for shift in range(0, 27):
        response = response + make_coded_message(message, shift)
        response = response + "<br>"
    response = response + "</pre>"
    return HttpResponse(response)


