from django.http import HttpResponse

def message(request):
    message = "Happy Birthday Laurence<p>"
    
    message = message + "<a href = http://jeanflower.pythonanywhere.com/laurence/messages>click here for a longer message!</a><p>"
    url = 'http://jeanflower.pythonanywhere.com/laurence/codes/hello/0'
    message = message + "Or go to <a href = '"+url+"'>"+url+"</a><p>"
    message = message + "Try things other than hello and 0."
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
        # if numbers became more than 97 (e.g. z would go to more)
        # wrap the numbers back using modulo arithmetic
        # now all our letters are between 0 and 96
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


