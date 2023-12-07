from django.http import HttpResponse, HttpResponseRedirect
import random
from .models import Scales,GenetUsers, Prototype2Questions, GenetUsers2, Prototype3Questions, GenetUsers3, GenetUsersClassification
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.utils import timezone 
#import csv
# Create your views here.

def informed_consent(request):
    
    request.session['question']="0"
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
    
    informed_consent_page="""<html>
<head>
<style>
H2 {text-align: center}
H3 {font-family:"arial";
    text-align:center;
}
P.center {font-family:"arial";
        text-align:center;
}
div.content{min-height: 100%%}
div.black{font-family:"arial";
        background: black;
        height:100px;
        color: white;
        text-align: center
}
div{
     font-family:"arial";
}
</style>
<title> Ethics statement and informed consent</title>
</head>
<body>
<div class="black">
<br>
<h2>DEPARTMENT OF COMPUTER SCIENCE</h2>
</div>
<div class='content'>
<div CLASS="border">
<p class="center"> UNIVERSITY OF CAPE TOWN
<br>
PRIVATE BAG X3
<br>
RONDEBOSCH 7701
<br>
SOUTH AFRICA
</p>
<p class="center"> RESEARCHER/S: Mr Kyle Seakgwa </p>
<p class="center">----------------------------------------------------------------------------------------------</p>
<h3>Informed Voluntary Consent to Participate in Research Study</h3>
<br>
<p class="center">Project Title : Developing an Elicitation Tool for Eliciting Users’ Moral Theories for Automated Moral Agents</p>
<br>
<p>Invitation to participate, and benefits: You are invited to participate in a research study conducted with professional philosophers and non-philosophers. The study's aim is to adjudicate between 3 computationally instantiated approaches to eliciting users’ moral theories, and thereby develop a computational tool which is able to categorize users according to their preferred moral theory.

I believe that your experience would be a valuable source of information, and hope that by participating you may gain useful knowledge.</p>

<p>Procedures: During this study, you will be asked to visit a website where you will be randomly assigned one of three prototypes to interact with. Depending on the prototype assigned, you will either be presented with questions, thought experiments or scenarios designed to elicit moral intuitions. The moral intuitions embodied in your responses will then be used by the protype to infer the your preferred moral theory.</p>

<p>Risks: There are no potentially harmful risks related to your participation in this study.</p>

<p>Feedback: You will receive feedback about the results of this research in the following manner: The prototype will display which ethical theory you were categorized as having.</p>

<p>Disclaimer/Withdrawal: Your participation is completely voluntary; you may refuse to participate, and you may withdraw at any time without having to state a reason and without any prejudice or penalty against you. Should you choose to withdraw, the researcher commits not to use any of the information you have provided without your signed consent. Note that the researcher may also withdraw you from the study at any time.</p>

<p>Confidentiality: All information collected in this study will be kept private in that you will not be identified by name or by affiliation to an institution. Confidentiality and anonymity will be maintained as pseudonyms will be used.</p>

<p>What signing this form means: By signing this consent form, you agree to participate in this research study. The aim, procedures to be used, as well as the potential risks and benefits of your participation have been explained verbally to you in detail, using this form. Refusal to participate in or withdrawal from this study at any time will have no effect on you in any way. You are free to contact me, to ask questions or request further information, at any time during this research.</p>
<form method="POST" action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/consent_check/">
%s
<br> 
I agree to participate in this research (click of the options): 
Yes<input type="radio" name="participation_status" value="Yes">
No<input type="radio" name="participation_status" value="No">
<input type=hidden name="questions" value="">
<br>
Name of Participant: <input type="text" name="full_name" value="your_full_name"> 
<br>
Signature of Participant(Initials):<input type="text" name="signature" value="your_signature_here">
<br>
Date:<input type="date" name= "date" value=%s>
<br>
<input type="hidden" name="prototype_ids">

<input type="submit">
</form>
</div>
</div>
<br>
<div class= "black">
<br>
<br>
<br>
<br>
Kyle Seakgwa(c)
<br>
<br>
</div>
</body>
</html>"""%(csrf_token_html,timezone.now())

    return HttpResponse(informed_consent_page)

@csrf_exempt
def consent_check(request):
    
    if request.POST['participation_status']=='Yes':
        
        request.session["full_name"]=request.POST["full_name"]
        request.session["date"]= request.POST["date"]
        
        prototype_ids=[1,2,3]
        prototype_ids=random.choice(prototype_ids)
        request.session["prototype_ids"]=prototype_ids
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/start_prototype/")
    
    else:
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/thank_you/")


def prototype_start(request):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
    
    if request.session["prototype_ids"]== 1:
        
        GenetUsers.objects.create(name=request.session["full_name"], date=request.session["date"])
        sc=Scales.objects.all().values("question_text", "scale_name")
        
        ous=Scales.objects.filter(scale_name='"ous"') | Scales.objects.filter(scale_name="ous")
        
        ous_list=[]
 
        for question in ous:
        
            question=str(question)
            ous_list.append(question)
    
        mda=Scales.objects.filter(scale_name='"mda"')| Scales.objects.filter(scale_name="mda")
        
        mda_list=[]

        for question in mda:
        
            question=str(question)
            mda_list.append(question)
   
        es=Scales.objects.filter(scale_name='"es"')| Scales.objects.filter(scale_name='"es"\r\n')| Scales.objects.filter(scale_name="es")
    
        es_list=[]

        for question in es:
        
            question=str(question)
            es_list.append(question)
    
        random.shuffle(ous_list)
        random.shuffle(mda_list)
        random.shuffle(es_list)
        
        scales=[mda_list, ous_list, es_list]
    
        random.shuffle(scales)
    
        request.session["ous"]=ous_list
        request.session["mda"]=mda_list
        request.session["es"]=es_list
        request.session["scales"]=scales
        request.session["ous_score"]=0
        request.session["mda_score"]=0
        request.session["es_score"]=0
        request.session["attention_checker"]=[]
        request.session["question_no1"]=0
        request.session["questions"]=[]
        request.session["answers"]=[]
        
        return HttpResponse("""<html><style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height: 100px
                                }
                                div.content{
                                min-height: 100%%
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:100px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                              </style>
                              
              <head><title>Welcome to prototype testing</title></head>
              <body>
              <div class="black">
              <br>
              <H2>
              Welcome to Genet Elicitation Tool Testing
              </H2>
              </div>
              <br>
              <div class= "content">
              <p> Thank you for your consent and participation. 
              Please click the button below to start the testing process</p>
              <br>
              
              <form method='post' action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/">
              %s
              <p><input type='submit' value='Start prototype'></p>
              </form>
              
              </div>
              <div class="footer-bottom">
              <br>
              <br>
              <br>
              <br>
                       Kyle Seakgwa(c)
              <br>
              </div>
              </body>
              </html>"""%(0,0,1,csrf_token_html))
    
    if request.session["prototype_ids"]== 2:
        
        GenetUsers.objects.create(name=request.session["full_name"], date=request.session["date"])
        
        mfq_questions=Prototype2Questions.objects.all()
         
        mfq_question_list=[]
 
        for question in mfq_questions:
        
            question=str(question)
            mfq_question_list.append(question)
    
        random.shuffle(mfq_question_list)
        
        request.session['mfq_items']=mfq_question_list
        request.session["care_score"]=0
        request.session["fairness_score"]=0
        request.session["loyalty_score"]=0
        request.session["authority_score"]=0
        request.session["sanctity_score"]=0
        request.session["liberty_score"]=0
        request.session["attention_check_2"]=[]
        request.session["questions"]=[]

        request.session["answers"]=[]
        
        return HttpResponse("""<html><style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height: 110px
                                }
                                div.content{
                                min-height: 100%%}
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:110px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                              </style>
              <head><title>Welcome to prototype testing</title></head>
              <body>
              <div class="black">
              <br>
              <H2>
              Welcome to Genet Elicitation Tool Testing
              </H2>
              </div>
              <br>
              <div class="content">
              <p> Thank you for your consent and participation. 
              Please click the button below to start the testing process</p>
              <br>
              
              <form method='post' action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/">
              %s
              <p><input type='submit' value='Start prototype'></p>
              </form>
              
              </div>
              <br>
              <br>
              <br>
              <div class=footer-bottom>
              <br>
              <div>
              <br>
              <br>
              <br>
              <br>
                       Kyle Seakgwa(c)
              <br>
              </div>
              </div>
              </body>
              </html>"""%(0, csrf_token_html))
        
    if request.session["prototype_ids"]== 3:    
        
        GenetUsers.objects.create(name=request.session["full_name"], date=request.session["date"])
        
        prototype_3_questions=Prototype3Questions.objects.filter().values()
        
        prototype_3_questions_list=[]
        
        for question in prototype_3_questions:
            
            prototype_3_questions_list.append(question)
            
        random.shuffle(prototype_3_questions_list)
        
        request.session["prototype_3_questions"]= prototype_3_questions_list
        request.session["utilitarianism_score"]=0
        request.session["egoism_score"]=0
        request.session["dct_score"]=0
        request.session["kantianism_score"]=0
        request.session["attention_check_3"]=[]
        request.session["questions"]=[]
        request.session["answers"]=[]
        
        return HttpResponse("""<html><style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height: 100px
                                }
                                div.content{
                                min-height: 100%%}
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:100px;
                                width:100%%;
                                position:absolute;
                                text-align: center
                                }
                              </style>
              <head><title>Welcome to prototype testing</title></head>
              <body>
              <div class= "black">
              <br>
              <H2>
              Welcome to Genet Elicitation Tool Testing
              </H2>
              </div>
              <br>
              <div class= "content">
              <p> Thank you for your consent and participation. 
              Please click the button below to start the testing process</p>
              <br>
              
              <form method='post' action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_3/">
              %s
              <p><input type='submit' value='Start prototype'></p>
              </form>
              <br>
              <br>
              </div>
              <br>
              <div class="footer-bottom">
              <br>
              <br>
              <br>
              <br>
                       Kyle Seakgwa(c)
              <br>
              </div>
              </body>
              </html>"""%(0,csrf_token_html))
        
@csrf_exempt
def scale_id_gate(request,scale_id, question_id, question_no):
    
    if scale_id<=2:
      
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/questions/"%(scale_id, question_id,question_no))
    
    elif scale_id==3:
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/results")
        
          
def participation_declined(request):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
    
    return HttpResponse("""<html>
                        <style>
                                H2 {text-align: center;
                                background: black;
                                color: white;}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                position: absolute;
                                height:100px;
                                width:100%%
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%;
                                position:absolute;
                                text-align: center}
                              </style>
              <head><title>Thank you for your interest</title></head>
              <body>
              
              <h2> Thank you for your interest in the project.</h2>
              
              <div class="content">
              <p>Since you have denied consent, you will not interact with any of the prototypes</p>
              </div>
              
              <div class=footer-bottom>
              <br>
                       Kyle Seakgwa(c)
              <br>
              </div>
              </body>
              
              </html>""")
    

def administer_scales(request,scale_id, question_id,question_no):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
        
    ous_questions= request.session["ous"]
    mda_questions=request.session["mda"]
    es_questions=request.session["es"]
    scales=request.session["scales"]
    es=Scales.objects.filter(pk=37).values()    
    
    if scales[scale_id] == mda_questions:
        
        request.session["questions"].append(mda_questions[question_id])      
        request.session.modified= True
        question_text= mda_questions[question_id].strip('""') 
        return HttpResponse("""<html>
                                <style>
                                H2 {text-align: center;
                                background: black;
                                color: white}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                div.content{min-height:100%%}
                                P {font-family:"arial";
                                text-align:center;
                                }
                                .black{font-family:"arial";
                                background: black;
                                color: white;
                                width:100%%;
                                height:150px

                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                                 
                              </style>
                       <head><title>Prototype 1</title></head>
                       <body>
                       <div class="black">
                       <br>
                       <h2>Prototype 1</h2>
                       </div>
                       <div class=content>
                       <h3>%s of 37</h3>
                       <br>
                       <p>Consider the following scenario:</p>
                       <br>
                       <p>%s</p>
                       <br>
                       
                       <form method="POST" action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/answers/">
                       %s
                       <p>On a scale of 1 (not wrong at all) to 9 (very wrong), how much do you agree with the statement above?</p>
                       <br>
                       <p><input type="number" min="1" max="9" step="1" name='answer'>
                       <br>
                       <input type= "submit"></p>
                       <br>
                       </form>
                       </div>
                       <div class="black">
                      
                       This prototype is based on psychological scales published in the following articles:
                        <ul class= "black">
                        <li>G. Kahane et al., “Beyond sacrificial harm: A two-dimensional model of utilitarian psychology.,” 
                           Psychol. Rev., vol. 125, no. 2, p. 131, 2018.</li>
                        <li>A. Simpson, J. Piazza, and K. Rios, “Belief in divine moral authority: Validation of a shortened scale with implications for social attitudes and moral cognition,”
                           Pers. Individ. Dif., vol. 94, pp.256–265, 2016.</li>
                        <li>R. H. Weigel, D. J. Hessing, and H. Elffers, “Egoism: Concept, measurement and implications for deviance,”
                           Psychol. Crime Law, vol. 5, no. 4, pp. 349–378, 1999.</li>
                       </ul>
                       </div>
                       
                       <div class= "footer-bottom">
                       <br>
                       <br>
                       <br>
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                       </body>
                       </html>"""%(question_no, question_text ,scale_id, question_id,question_no,csrf_token_html))
        
                       
        
    if scales[scale_id] == ous_questions:        
        
        request.session["questions"].append(ous_questions[question_id])                
        request.session.modified= True
        
        question_text= ous_questions[question_id].strip('""')
        
        return HttpResponse("""<html>
                                <style>
                                H2 {text-align: center;
                                background: black;
                                color: white}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{
                                min-height: 100%%}
                                .black{font-family:"arial";
                                background: black;
                                color: white;
                                width:100%%;
                                height:150px
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center
                                }
                              </style>
                       <head><title>Prototype 1</title></head>
                       <body>
                       <div class="black">
                       <br>
                       <h2>Prototype 1</h2>
                       </div>
                       <div class= content>
                       <h3>%s of 37</h3>
                       <br>
                       <p>Consider the following scenario:</p>
                       <br>
                       <p>%s</p>
                       <br>
                       <form method="POST" action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/answers/">
                       %s
                       <p>On a scale of 1 (not wrong at all) to 7 (very wrong), how much do you agree with the statement above?</p>
                       <br>
                       <p><input type="number" min="1" max="9" step="1" name='answer'>
                       <br>
                       <input type= "submit"></p>
                       
                       </form>
                       </div>
                       <div class="black">
                       <br>
                       <br>
                      
                       This prototype is based on psychological scales published in the following articles:
                        <ul class= black>
                        <li>G. Kahane et al., “Beyond sacrificial harm: A two-dimensional model of utilitarian psychology.,” 
                           Psychol. Rev., vol. 125, no. 2, p. 131, 2018.</li>
                        <li>A. Simpson, J. Piazza, and K. Rios, “Belief in divine moral authority: Validation of a shortened scale with implications for social attitudes and moral cognition,”
                           Pers. Individ. Dif., vol. 94, pp.256–265, 2016.</li>
                        <li>R. H. Weigel, D. J. Hessing, and H. Elffers, “Egoism: Concept, measurement and implications for deviance,”
                           Psychol. Crime Law, vol. 5, no. 4, pp. 349–378, 1999.</li>
                       </ul>
                       </div>
                       <div class= "footer-bottom">
                       <br>
                       <br>
                       <br>
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                       </body>
                       </html>"""%(question_no,question_text,scale_id, question_id,question_no ,csrf_token_html))
        
                       
    if scales[scale_id] == es_questions:
           
        request.session["questions"].append(es_questions[question_id])
        request.session.modified= True
        question_text= es_questions[question_id].strip('""')
        return HttpResponse("""<html>
                                <style>
                                H2 {text-align: center;
                                background: black;
                                color: white;
                                }
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                .black{font-family:"arial";
                                background: black;
                                color: white;
                                width:100%%;
                                height:150px;

                                }
                                div.content{
                                min-height: 100%%}
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center
                                }
                              </style>
                       <head><title>Prototype 1</title></head>
                       <body>
                       <div class="black">
                       <br>
                       <h2>Prototype 1</h2>
                       </div>
                       <div class=content>
                       <h3>%s of 37</h3>
                       <br>
                       <p>Consider the following scenario:</p>
                       <br>
                       <p>%s</p>
                       <br>
                       
                       <form method="POST" action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/answers/">

                       %s
                       <p>On a scale of 1 (not wrong at all) to 5 (very wrong), how much do you agree with the statement above?</p>
                       <br>
                       <p><input type="number" min="1" max="9" step="1" name='answer'>
                       <br>
                       <input type= "submit"></p>
                       </form>
                       </div>
                       <div class="black">
                       <br>
    
                       This prototype is based on psychological scales published in the following articles:
                        <ul class= black>
                        <li>G. Kahane et al., “Beyond sacrificial harm: A two-dimensional model of utilitarian psychology.,” 
                           Psychol. Rev., vol. 125, no. 2, p. 131, 2018.</li>
                        <li>A. Simpson, J. Piazza, and K. Rios, “Belief in divine moral authority: Validation of a shortened scale with implications for social attitudes and moral cognition,”
                           Pers. Individ. Dif., vol. 94, pp.256–265, 2016.</li>
                        <li>R. H. Weigel, D. J. Hessing, and H. Elffers, “Egoism: Concept, measurement and implications for deviance,”
                           Psychol. Crime Law, vol. 5, no. 4, pp. 349–378, 1999.</li>
                       </ul>
                       </div>
                       <div class="footer-bottom"> 
                       <br>
                       <br>
                       <br>
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                       </body>
                       </html>"""%(question_no,question_text, scale_id, question_id, question_no, csrf_token_html))
                    
                       
@csrf_exempt                
def answers(request,scale_id, question_id,question_no):

    answer=request.POST["answer"]
    
    if answer=='':
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/questions/"%(scale_id, question_id,question_no))
    
    elif answer<"1":
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/questions/"%(scale_id, question_id,question_no))
            
    ous_questions= request.session["ous"]
    mda_questions=request.session["mda"]
    es_questions=request.session["es"]
    scales=request.session["scales"]
    
    if scales[scale_id] == ous_questions and answer>"7":
    
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/questions/"%(scale_id, question_id,question_no))
    
    elif scales[scale_id] == mda_questions and answer>"9":
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/questions/"%(scale_id, question_id,question_no))
    
    elif scales[scale_id] == es_questions and answer>"5":
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/questions/"%(scale_id, question_id,question_no))
    
    try:
        
        answer=int(answer)
        
    except ValueError:
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/%s/questions/"%(scale_id, question_id,question_no))
    
    
    request.session["answers"].append(answer)
    request.session.modified= True
    
    if scales[scale_id] == mda_questions and question_id<= 4:
        if scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."' or scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."':
        
            if (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."' and answer==3) or (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."' and answer==1):
            
                request.session["attention_checker"].append("Yes")
                request.session.modified= True 
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id, question_id+1,question_no+1))
            else:
                request.session["attention_checker"].append("No")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id, question_id+1,question_no+1))
    
    elif scales[scale_id] == mda_questions and question_id >= 5:
        if scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."' or scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."':

            if (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."' and answer==3) or (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."' and answer==1):

                request.session["attention_checker"].append("Yes")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id+1, 0,question_no+1))

            else:
                request.session["attention_checker"].append("No")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id+1, 0,question_no+1))

    elif scales[scale_id] == es_questions and question_id<= 19:
        if scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."' or scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."': 
        
            if (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."' and answer==3) or (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."' and answer==1):
            
                request.session["attention_checker"].append("Yes")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id, question_id+1,question_no+1))
            else:
                request.session["attention_checker"].append("No")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id, question_id+1,question_no+1))
    
    elif scales[scale_id] == es_questions and question_id >= 20:
        if scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."' or scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."':
        
            if (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."' and answer==3) or (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."' and answer==1):
            
                request.session["attention_checker"].append("Yes")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id+1, 0,question_no+1))
            else:
                request.session["attention_checker"].append("No")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id+1, 0,question_no+1))
    
    elif scales[scale_id] == ous_questions and question_id<=8:
        if scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."' or scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."':
            if (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."' and answer==3) or (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."' and answer==1):
                request.session["attention_checker"].append("Yes")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id, question_id+1,question_no+1))                                           
            else:
                
                request.session["attention_checker"].append("No")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id, question_id+1,question_no+1))
    elif scales[scale_id] == ous_questions and question_id>=9:
        if scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."' or scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."':
            if (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."' and answer==3) or (scales[scale_id][question_id]== '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."' and answer==1):
                
                request.session["attention_checker"].append("Yes")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id+1, 0,question_no+1))                                         
            else:                                                                                                                                                                       
                request.session["attention_checker"].append("No")
                request.session.modified= True
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id+1, 0,question_no+1)) 

    if scales[scale_id] == ous_questions and question_id<=8:
        if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."':
            if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."':   
                request.session["ous_score"]+=answer
        
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id, question_id+1,question_no+1))
    
    elif scales[scale_id] == mda_questions and question_id<= 4:
         if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."':
             if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."':
                 request.session["mda_score"]+=answer
        
                 return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id, question_id+1,question_no+1))
   
    elif scales[scale_id] == es_questions and question_id<= 19:
         if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."':
             if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."': 
                 request.session["es_score"]+=answer
        
                 return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id, question_id+1,question_no+1))
    
    elif scales[scale_id] == ous_questions and question_id >= 9:
        if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."': 
            if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."': 
                request.session["ous_score"]+=answer
                
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id+1, 0,question_no+1))
     
    elif scales[scale_id] == mda_questions and question_id >= 5:
        if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."': 
            if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."': 
                request.session["mda_score"]+=answer
                
        
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id+1, 0,question_no+1))
    
    elif scales[scale_id] == es_questions and question_id >= 20:
        if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."':
            if scales[scale_id][question_id]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 1 on the scale below."': 
                request.session["es_score"]+=answer
                
                return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/%s/%s/checker/"%(scale_id+1, 0,question_no+1))


def results(request):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
    
    ous_score= request.session["ous_score"]
    mda_score= request.session["mda_score"]
    es_score= request.session["es_score"] 
    
    
    ous_questions= request.session["ous"]                                                                                                                                   
    mda_questions=request.session["mda"]                                                                                                                                    
    es_questions=request.session["es"]
    mean_ous= (ous_score)/len(ous_questions)
    percentage_ous= (mean_ous/7)*100
    mean_mda= (mda_score)/len(mda_questions) 
    percentage_mda= (mean_mda/9)*100
    mean_es= (es_score)/len(es_questions)
    percentage_es= (mean_es/5)*100
    
    if percentage_ous<50 and percentage_mda<50:
        if percentage_es<50:
            
            result="You are a deontologist"
            
    elif percentage_ous> percentage_mda and percentage_ous>percentage_es:
        if percentage_ous>50:
            
            result="You are a utilitarian"
        
    elif percentage_ous<percentage_mda and percentage_mda>percentage_es: 
        if percentage_mda>50:
        
            result= "You are a divine command theorist"
     
    elif percentage_es> percentage_mda and percentage_es>percentage_ous:
        if percentage_es>=25:
               
            result= "You are an egoist"
    
    elif percentage_es==percentage_mda and percentage_ous== percentage_ous:
        if percentage_ous>50:
            
            result="Your moral theory is not ascertainable by Genet at this time"
    else:
        result="Your moral theory is not ascertainable by Genet at this time"
     
    try:
        print(result)
    
    except:
        
        result="You are an egoist"
    
    #with open("prototype_1_data.csv", "w") as prototype_1_data:
        
        #writer= csv.writer(prototype_1_data)
        #writer.writerow(ous_percentage, percentage_mda, percentage_es, result)


    if request.session["attention_checker"][0]=="Yes" and request.session["attention_checker"][1]=="Yes" and request.session["attention_checker"][2]=="Yes": 
        
    
        GenetUsersClassification.objects.create(user_classification=result, attention_check="Passed",question_1=request.session["questions"][0],answer_1=request.session["answers"][0],question_2=request.session["questions"][1],answer_2=request.session["answers"][1],question_3=request.session["questions"][2],answer_3=request.session["answers"][2],question_4=request.session["questions"][3],answer_4=request.session["answers"][3],question_5=requesti.session["questions"][4],answer_5=request.session["answers"][4],question_6=request.session["questions"][5],answer_6=request.session["answers"][5],question_7=request.session["questions"][6],answer_7=request.session["answers"][6],question_8=request.session["questions"][7],answer_8=request.session["answers"][7],question_9=request.session["questions"][8],answer_9=request.session["answers"][8],question_10=request.session["questions"][9],answer_10=request.session["answers"][9],question_11=request.session["questions"][10],answer_11=request.session["answers"][10],question_12=request.session["questions"][11],answer_12=request.session["answers"][11],question_13=request.session["questions"][12],answer_13=request.session["answers"][12],question_14=request.session["questions"][13],answer_14=request.session["answers"][13],question_15=request.session["questions"][14],answer_15=request.session["answers"][14],question_16=request.session["questions"][15],answer_16=request.session["answers"][15],question_17=request.session["questions"][16],answer_17=request.session["answers"][16],question_18=request.session["questions"][17],answer_18=request.session["answers"][17],question_19=request.session["questions"][18],answer_19=request.session["answers"][18],question_20=request.session["questions"][19],answer_20=request.session["answers"][19],question_21=request.session["questions"][20],answer_21=request.session["answers"][20],question_22=request.session["questions"][21],answer_22=request.session["answers"][21],question_23=request.session["questions"][22],answer_23=request.session["answers"][22],question_24=request.session["questions"][23],answer_24=request.session["answers"][23],question_25=request.session["questions"][24],answer_25=request.session["answers"][24],question_26=request.session["questions"][25],answer_26=request.session["answers"][25],question_27=request.session["questions"][26], answer_27=request.session["answers"][26],question_28=request.session["questions"][27],answer_28=request.session["answers"][27],question_29=request.session["questions"][28],answer_29=request.session["answers"][28],question_30=request.session["questions"][29],answer_30=request.session["answers"][27],question_31=request.session["questions"][30], answer_31=request.session["answers"][30],question_32=request.session["questions"][31],answer_32=request.session["answers"][31],question_33=request.session["questions"][32],answer_33=request.session["answers"][32],question_34=request.session["questions"][33],answer_34=request.session["answers"][33],question_35=request.session["questions"][34],answer_35=request.session["answers"][34],question_36=request.session["questions"][35],answer_36=request.session["answers"][35],question_37=request.session["questions"][36],answer_37=request.session["answers"][36])
    
        current_user= GenetUsersClassification.objects.last()
        
        return HttpResponse("""<html>
                        <style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height:150px;
                                width:100%%
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:50px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                                }
                              </style>
                        <head><title>result</title></head>
                        
                        <body>
                        <div class= black>
                        <br>
                        <h2>Result</h2>
                        </div>
                        <div class=content>
                        <br>
                        <br>
                         <p> Please remember the following information (write it down if necessary):</p>
                        <br>
                        <br>
                        <br>
                        <p>%s</p>
                        <br>
                        <br>
                        <br>
                        <p>Your participant number is: %s</p>
                        <br>
                        <p> The prototype you interacted with was: Prototype 1 </p>
                        <br>
                        <form action="https://survey.cs.uct.ac.za/limesurvey/index.php/445565?lang=en">
                        <p>Click the button below to continue to the next part of the study</p>
                        <br>
                        <center><input type="submit" value= "Continue"/></center>
                        <br>

                        <br>
                        <br>
                        <br>
                        </div>
                        %s
                        <br>
                        <div class="black">
                       <br>
                       
                       This prototype is based on psychological scales published in the following articles:
                        <ul class= black>
                        <li>G. Kahane et al., “Beyond sacrificial harm: A two-dimensional model of utilitarian psychology.,” 
                           Psychol. Rev., vol. 125, no. 2, p. 131, 2018.</li>
                        <li>A. Simpson, J. Piazza, and K. Rios, “Belief in divine moral authority: Validation of a shortened scale with implications for social attitudes and moral cognition,”
                           Pers. Individ. Dif., vol. 94, pp.256–265, 2016.</li>
                        <li>R. H. Weigel, D. J. Hessing, and H. Elffers, “Egoism: Concept, measurement and implications for deviance,”
                           Psychol. Crime Law, vol. 5, no. 4, pp. 349–378, 1999.</li>
                       </ul>
                       </div>
                        <div class= "footer-bottom">
                        <br>
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                        </body>
                        </html>"""%(result,current_user, csrf_token_html))


        
        
    
    else:
        

        GenetUsersClassification.objects.create(user_classification=result, attention_check="Failed",question_1=request.session["questions"][0],answer_1=request.session["answers"][0],question_2=request.session["questions"][1],answer_2=request.session["answers"][1],question_3=request.session["questions"][2],answer_3=request.session["answers"][2],question_4=request.session["questions"][3],answer_4=request.session["answers"][3],question_5=request.session["questions"][4],answer_5=request.session["answers"][4],question_6=request.session["questions"][5],answer_6=request.session["answers"][5],question_7=request.session["questions"][6],answer_7=request.session["answers"][6],question_8=request.session["questions"][7],answer_8=request.session["answers"][7],question_9=request.session["questions"][8],answer_9=request.session["answers"][8],question_10=request.session["questions"][9],answer_10=request.session["answers"][9],question_11=request.session["questions"][10],answer_11=request.session["answers"][10],question_12=request.session["questions"][11],answer_12=request.session["answers"][11],question_13=request.session["questions"][12],answer_13=request.session["answers"][12],question_14=request.session["questions"][13],answer_14=request.session["answers"][13],question_15=request.session["questions"][14],answer_15=request.session["answers"][14],question_16=request.session["questions"][15],answer_16=request.session["answers"][15],question_17=request.session["questions"][16],answer_17=request.session["answers"][16],question_18=request.session["questions"][17],answer_18=request.session["answers"][17],question_19=request.session["questions"][18],answer_19=request.session["answers"][18],question_20=request.session["questions"][19],answer_20=request.session["answers"][19],question_21=request.session["questions"][20],answer_21=request.session["answers"][20],question_22=request.session["questions"][21],answer_22=request.session["answers"][21],question_23=request.session["questions"][22],answer_23=request.session["answers"][22],question_24=request.session["questions"][23],answer_24=request.session["answers"][23],question_25=request.session["questions"][24],answer_25=request.session["answers"][24],question_26=request.session["questions"][25],answer_26=request.session["answers"][25],question_27=request.session["questions"][26], answer_27=request.session["answers"][26],question_28=request.session["questions"][27],answer_28=request.session["answers"][27],question_29=request.session["questions"][28],answer_29=request.session["answers"][28],question_30=request.session["questions"][29],answer_30=request.session["answers"][27],question_31=request.session["questions"][30], answer_31=request.session["answers"][30],question_32=request.session["questions"][31],answer_32=request.session["answers"][31],question_33=request.session["questions"][32],answer_33=request.session["answers"][32],question_34=request.session["questions"][33],answer_34=request.session["answers"][33],question_35=request.session["questions"][34],answer_35=request.session["answers"][34],question_36=request.session["questions"][35],answer_36=request.session["answers"][35],question_37=request.session["questions"][36],answer_37=request.session["answers"][36])
        
        current_user= GenetUsersClassification.objects.last()

             
        return HttpResponse("""<html>
                        <style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height:150px;
                                width:100%%
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:50px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                                }
                              </style>
                        <head><title>result</title></head>
                        
                        <body>
                        <div class= black>
                        <br>
                        <h2>Result</h2>
                        </div>
                        <div class=content>
                        <br>
                        <br> 
                        <br>
                        <br>
                        <br>
                        <p>%s</p>
                        <br>
                        <br>
                        <br>
                        <p>Your participant number is: %s</p>
                        <br>
                        <p> The prototype you interacted with was: Prototype 1 </p>
                        <br>
                        <br>
                        <br>
                        <br>
                        </div>
                        %s
                        <br>
                        <br>
                        <br> 
                        <br>
                        <div class="black">
                       <br>
                       <br>
                       
                       This prototype is based on psychological scales published in the following articles:
                        <ul class= black>
                        <li>G. Kahane et al., “Beyond sacrificial harm: A two-dimensional model of utilitarian psychology.,” 
                           Psychol. Rev., vol. 125, no. 2, p. 131, 2018.</li>
                        <li>A. Simpson, J. Piazza, and K. Rios, “Belief in divine moral authority: Validation of a shortened scale with implications for social attitudes and moral cognition,”
                           Pers. Individ. Dif., vol. 94, pp.256–265, 2016.</li>
                        <li>R. H. Weigel, D. J. Hessing, and H. Elffers, “Egoism: Concept, measurement and implications for deviance,”
                           Psychol. Crime Law, vol. 5, no. 4, pp. 349–378, 1999.</li>
                       </ul>
                       </div>
                        <div class= "footer-bottom">
                        <br>
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                        </body>
                        </html>"""%(result,current_user, csrf_token_html))

@csrf_exempt
def prototype_2_adminster_questions(request, question_id):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
    
    mfq_questions=request.session["mfq_items"]
    request.session.modified= True 
    
    try:
       question_text= mfq_questions[question_id].strip('""') 
       request.session["questions"].append(mfq_questions[question_id])
       
       return HttpResponse("""<html>
                                <style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height:110px
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                                }
                              </style>
                       <head><title>Prototype 2</title></head>
                       <body>
                       <div class= black>
                       <br>
                       
                       <h2>Prototype 2</h2>
                       </div>
                       <div class= content>
                       <h3>%s of 34</h3>
                       <body>
                       <p>Consider the following scenario:</p>
                       <br>
                       <p>%s</p>
                       <br>
                       <form method="POST" action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/answers_2/">
                       %s
                       <p>On a scale of 1 (not wrong at all) to 5 (very wrong), how morally wrong is the situation described above?</p>
                       <br>
                       <p><input type="number" min="1" max="5" step="1" name='answer_2'>
                       <br>
                       <input type= "submit"></p>
                       </form>
                       </div>
                       <br>
                       <br>
                       <br>
                       <br>
                       <br>
                       <br>
                       
                       <br>
                       <div class= black>
                       <br>
                       This prototype is based on psychological scales published in the following articles:
                       <ul>
                       <li>
                       D. L. Crone and S. M. Laham, “Multiple moral foundations predict responses to sacrificial dilemmas,” Pers. Individ. Dif., vol. 85, pp. 60–65, 2015.
                       </li>
                       <li>
                       Clifford, V. Iyengar, R. Cabeza, and W. Sinnott-Armstrong, “Moral foundations vignettes: A standardized stimulus database of scenarios based on moral foundations theory,” Behav. Res. Methods, vol. 47, no. 4, pp. 1178–1198, 2015.
                       </li>
                       </ul>
                       </div>
                       <div class=footer-bottom>
                       <br>
                       <br>
                       <br>
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                       </body>
                       </html>"""%(question_id+1,question_text, question_id, csrf_token_html))

            
    except IndexError:
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/results_2/")

@csrf_exempt
def prototype_2_answers(request,question_id):
    
    answer=request.POST["answer_2"]
    
    if answer=='':
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id))
        
    if answer<"1" or answer>"5":
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id))
    
    mfq_questions=request.session["mfq_items"]
    
    mfq_questions_as_values=Prototype2Questions.objects.filter(question_text=mfq_questions[question_id]).values("question_type","question_text")
   
    try:
        
        answer=int(answer)
        
    except ValueError:
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id))
    
    request.session["answers"].append(answer)  
    request.session.modified= True
    
    if mfq_questions_as_values[0]['question_text']== '"This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below."':
        
        if answer==3:
            
            request.session["attention_check_2"].append("Yes")
            request.session.modified= True
        else:
            
            request.session["attention_check_2"].append("No")
            request.session.modified= True
       
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id+1))

    if mfq_questions_as_values[0]['question_text']== '"This is a control question to check whether you are paying attention. Please proceed by selecting 2 on the scale below."':
    
        if answer==2:
              
            request.session["attention_check_2"].append("Yes")
            request.session.modified= True
       
        else:

            request.session["attention_check_2"].append("No")
            request.session.modified= True
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id+1))

    if mfq_questions_as_values[0]['question_text']== '"This is a control question to check whether you are paying attention. Please proceed by selecting 4 on the scale below."':
        
        if answer==4:
                
            request.session["attention_check_2"].append("Yes")
            request.session.modified= True
        
        else:
            
            request.session["attention_check_2"].append("No")
            request.session.modified= True 
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id+1))

    if mfq_questions_as_values[0]['question_type'].strip('"\rn"')=="care":    
        
        if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 2 on the scale below.": 
            if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 4 on the scale below.":
                if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below.":    
                    request.session["care_score"]+=answer
        
                    return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id+1))
    
    if mfq_questions_as_values[0]['question_type'].strip('"\rn"')=="fairness":    
    
        if mfq_questions_as_values[0]['question_text']!= '"This is a control question to check whether you are paying attention. Please proceed by selecting 2 on the scale below."': 
            if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 4 on the scale below.":  
                if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below.": 
                    request.session["fairness_score"]+=answer
                    return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id+1))
    
    if mfq_questions_as_values[0]['question_type'].strip('"\rn"')=="loyalty":    
        
        if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 2 on the scale below.": 
            if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 4 on the scale below.":
                if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below.":
                    request.session["loyalty_score"]+=answer
                    return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id+1))
    
    if mfq_questions_as_values[0]['question_type'].strip('"\rn"')=="authority":    
        
        if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 2 on the scale below.": 
            if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 4 on the scale below.": 
                if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below.": 
                    request.session["authority_score"]+=answer
                    return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id+1))
    
    if mfq_questions_as_values[0]['question_type'].strip('"\rn"')=="sanctity":    
        
        if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= 'This is a control question to check whether you are paying attention. Please proceed by selecting 2 on the scale below.':             
            if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 4 on the scale below.":
                if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below.":     
                    request.session["sanctity_score"]+=answer
                    return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id+1))
    
    if mfq_questions_as_values[0]['question_type'].strip('"\rn"')=="liberty":    
    
        if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 2 on the scale below.":            
            if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 4 on the scale below.":     
                if mfq_questions_as_values[0]['question_text'].strip('"\rn"')!= "This is a control question to check whether you are paying attention. Please proceed by selecting 3 on the scale below.":  
                    request.session["liberty_score"]+=answer
                    return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_2/"%(question_id+1))

@csrf_exempt
def results_2(request):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
    
    care_score=request.session["care_score"]
    fairness_score=request.session["fairness_score"]
    loyalty_score=request.session["loyalty_score"]
    authority_score=request.session["authority_score"]
    sanctity_score=request.session["sanctity_score"]
    liberty_score=request.session["liberty_score"]
    
    care_score=care_score/6
    fairness_score=fairness_score/5
    loyalty_score=loyalty_score/5
    authority_score=authority_score/5
    sanctity_score=sanctity_score/5
    
    dilemma_score= 3.25+(-0.21*care_score)+(-0.09*fairness_score)+(0.04*loyalty_score)+(-0.04*authority_score)+(-0.16*sanctity_score)
    
    if loyalty_score>= 3.34 and authority_score>= 3.64 and sanctity_score>= 3.65 and dilemma_score<=1.58:
        
        result="You are a divine command theorist"

    elif loyalty_score<= 1.5 and care_score<=2.6 and fairness_score<=2.46 and authority_score<= 1.84 and sanctity_score<= 1.15:
        
        result="You are an egoist"

    elif dilemma_score>1.58:
        
        result= "You are a utilitarian"
    
    elif dilemma_score<1.58:
       
        result="You are a deontologist"
    
    if request.session["attention_check_2"][0]=="Yes" and request.session["attention_check_2"][1]=="Yes" and request.session["attention_check_2"][2]=="Yes": 
        
        GenetUsers2.objects.create(user_classification=result,attention_check="Passed",question_1=request.session["questions"][0],answer_1=request.session["answers"][0],question_2=request.session["questions"][1],answer_2=request.session["answers"][1],question_3=request.session["questions"][2],answer_3=request.session["answers"][2],question_4=request.session["questions"][3],answer_4=request.session["answers"][3],question_5=request.session["questions"][4],answer_5=request.session["answers"][4],question_6=request.session["questions"][5],answer_6=request.session["answers"][5],question_7=request.session["questions"][6],answer_7=request.session["answers"][6],question_8=request.session["questions"][7],answer_8=request.session["answers"][7],question_9=request.session["questions"][8],answer_9=request.session["answers"][8],question_10=request.session["questions"][9],answer_10=request.session["answers"][9],question_11=request.session["questions"][10],answer_11=request.session["answers"][10],question_12=request.session["questions"][11],answer_12=request.session["answers"][11],question_13=request.session["questions"][12],answer_13=request.session["answers"][12],question_14=request.session["questions"][13],answer_14=request.session["answers"][13],question_15=request.session["questions"][14],answer_15=request.session["answers"][14],question_16=request.session["questions"][15],answer_16=request.session["answers"][15],question_17=request.session["questions"][16],answer_17=request.session["answers"][16],question_18=request.session["questions"][17],answer_18=request.session["answers"][17],question_19=request.session["questions"][18],answer_19=request.session["answers"][18],question_20=request.session["questions"][19],answer_20=request.session["answers"][19],question_21=request.session["questions"][20],answer_21=request.session["answers"][20],question_22=request.session["questions"][21],answer_22=request.session["answers"][21],question_23=request.session["questions"][22],answer_23=request.session["answers"][22],question_24=request.session["questions"][23],answer_24=request.session["answers"][23],question_25=request.session["questions"][24],answer_25=request.session["answers"][24],question_26=request.session["questions"][25],answer_26=request.session["answers"][25],question_27=request.session["questions"][26], answer_27=request.session["answers"][26],question_28=request.session["questions"][27],answer_28=request.session["answers"][27],question_29=request.session["questions"][28],answer_29=request.session["answers"][28],question_30=request.session["questions"][29],answer_30=request.session["answers"][27],question_31=request.session["questions"][30], answer_31=request.session["answers"][30],question_32=request.session["questions"][31],answer_32=request.session["answers"][31],question_33=request.session["questions"][32],answer_33=request.session["answers"][32],question_34=request.session["questions"][33],answer_34=request.session["answers"][33]) 

        current_user= GenetUsers2.objects.last()

        return HttpResponse("""<html>
                        <style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height:110px
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                              </style>
                        <head><title>result</title></head>
                        
                        <body>
                        <div class=black>
                        <h2>Result:</h2>
                        </div>
                        <div class=content>
                        <br>
                        <br>
                        <br>
                         <p> Please remember the following information (write it down if necessary):</p>
                        <br>
                        <br>
                        <p>%s</p>
                        <br>
                        <br>
                        <br>
                        <br>
                        <p>Your participant number is: %s</p>
                        <br>
                        <p> The prototype you interacted with was: Prototype 2 </p>
                        <br>
                        <form action="https://survey.cs.uct.ac.za/limesurvey/index.php/445565?lang=en">
                        <p>Click the button below to continue to the next part of the study</p>
                        <br>
                        <center><input type="submit" value= "Continue"/></center>
                        <br>
                        </div>
                        <br>
                        <br> 
                        <br>
                        <br>
                        <div class= black>
                       <br>
                       This prototype is based on psychological scales published in the following articles:
                       <ul>
                       <li>
                       D. L. Crone and S. M. Laham, “Multiple moral foundations predict responses to sacrificial dilemmas,” Pers. Individ. Dif., vol. 85, pp. 60–65, 2015.
                       </li>
                       <li>
                       Clifford, V. Iyengar, R. Cabeza, and W. Sinnott-Armstrong, “Moral foundations vignettes: A standardized stimulus database of scenarios based on moral foundations theory,” Behav. Res. Methods, vol. 47, no. 4, pp. 1178–1198, 2015.
                       </li>
                       </ul>
                       </div>
                        <div class=footer-bottom>
                        <br>
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                        </body>
                        </html>"""%(result, current_user))
    else:

        GenetUsers2.objects.create(user_classification=result,attention_check="Failed",question_1=request.session["questions"][0],answer_1=request.session["answers"][0],question_2=request.session["questions"][1],answer_2=request.session["answers"][1],question_3=request.session["questions"][2],answer_3=request.session["answers"][2],question_4=request.session["questions"][3],answer_4=request.session["answers"][3],question_5=request.session["questions"][4],answer_5=request.session["answers"][4],question_6=request.session["questions"][5],answer_6=request.session["answers"][5],question_7=request.session["questions"][6],answer_7=request.session["answers"][6],question_8=request.session["questions"][7],answer_8=request.session["answers"][7],question_9=request.session["questions"][8],answer_9=request.session["answers"][8],question_10=request.session["questions"][9],answer_10=request.session["answers"][9],question_11=request.session["questions"][10],answer_11=request.session["answers"][10],question_12=request.session["questions"][11],answer_12=request.session["answers"][11],question_13=request.session["questions"][12],answer_13=request.session["answers"][12],question_14=request.session["questions"][13],answer_14=request.session["answers"][13],question_15=request.session["questions"][14],answer_15=request.session["answers"][14],question_16=request.session["questions"][15],answer_16=request.session["answers"][15],question_17=request.session["questions"][16],answer_17=request.session["answers"][16],question_18=request.session["questions"][17],answer_18=request.session["answers"][17],question_19=request.session["questions"][18],answer_19=request.session["answers"][18],question_20=request.session["questions"][19],answer_20=request.session["answers"][19],question_21=request.session["questions"][20],answer_21=request.session["answers"][20],question_22=request.session["questions"][21],answer_22=request.session["answers"][21],question_23=request.session["questions"][22],answer_23=request.session["answers"][22],question_24=request.session["questions"][23],answer_24=request.session["answers"][23],question_25=request.session["questions"][24],answer_25=request.session["answers"][24],question_26=request.session["questions"][25],answer_26=request.session["answers"][25],question_27=request.session["questions"][26], answer_27=request.session["answers"][26],question_28=request.session["questions"][27],answer_28=request.session["answers"][27],question_29=request.session["questions"][28],answer_29=request.session["answers"][28],question_30=request.session["questions"][29],answer_30=request.session["answers"][27],question_31=request.session["questions"][30], answer_31=request.session["answers"][30],question_32=request.session["questions"][31],answer_32=request.session["answers"][31],question_33=request.session["questions"][32],answer_33=request.session["answers"][32],question_34=request.session["questions"][33],answer_34=request.session["answers"][33])
        
        current_user= GenetUsers2.objects.last()                                                                                                                                                                                                                                                                                             
        return HttpResponse("""<html>
                        <style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height:110px
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                              </style>
                        <head><title>result</title></head>
                        
                        <body>
                        <div class=black>
                        <h2>Result:</h2>
                        </div>
                        <div class=content>
                        <br>
                        <br>
                        <br>
                        <br>
                        <br>
                        <br>
                        <p>%s</p>
                        <br>
                        <br>
                        <p>Your participant number is:%s</p>
                        <br>
                        <p> The prototype you interacted with was: Prototype 2 </p>

                        <br>
                        </div>
                        <br>
                        <div class= black>
                       <br>
                       This prototype is based on psychological scales published in the following articles:
                       <ul>
                       <li>
                       D. L. Crone and S. M. Laham, “Multiple moral foundations predict responses to sacrificial dilemmas,” Pers. Individ. Dif., vol. 85, pp. 60–65, 2015.
                       </li>
                       <li>
                       Clifford, V. Iyengar, R. Cabeza, and W. Sinnott-Armstrong, “Moral foundations vignettes: A standardized stimulus database of scenarios based on moral foundations theory,” Behav. Res. Methods, vol. 47, no. 4, pp. 1178–1198, 2015.
                       </li>
                       </ul>
                       </div>
                        <div class=footer-bottom>
                        <br>
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                        </body>
                        </html>"""%(result, current_user))
    
@csrf_exempt        
def prototype_3_adminster_questions(request, question_id):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
    
    prototype_3_questions=request.session["prototype_3_questions"]
    
    principles=["An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost.",
                "An action is right if its ends are in the agent's self-interest",
                "An action is right if God wills it so",
                "An action is right if it is universally willable and it respects the rational autonomy of others." 
               ]
    
    random.shuffle(principles)
    
    try:
        
        request.session["questions"].append(prototype_3_questions[question_id]["question_text"])
        request.session.modified= True
        if prototype_3_questions[question_id]["question_text"][0]=='"':
            question_text=prototype_3_questions[question_id]["question_text"][1:-3]
        else:
            question_text=prototype_3_questions[question_id]["question_text"]
        
        if question_text== 'This is a control question to check whether you are paying attention. Please proceed by selecting "An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost." on the scale belo':
            question_text='This is a control question to check whether you are paying attention. Please proceed by selecting "An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost." on the scale below.'

        return HttpResponse("""<html>
                                <style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height: 100px
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                                }
                              </style>
                       <head><title>Prototype 3</title></head>
                       <body>
                       <div class=black>
                       <br>
                       <h2>Prototype 3</h2>
                       </div>
                       <div class=content>
                       <h3>%s of 7</h3>
                       <body>
                       <p>Consider the following scenario:</p>
                       <p>%s</p>
                       <br>
                       <br>
                       <form method="POST" action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/answers_3/">
                       %s
                       <p>Which of the following principles would you apply to the situation described above?</p>
                       <br>
                       <br>
                       %s<input type="radio" name="answer_3" value="%s">
                       <br>
                       <br>
                       %s<input type="radio" name="answer_3" value="%s">
                       <br>
                       <br>
                       %s<input type="radio" name="answer_3" value="%s">
                       <br>
                       <br>
                       %s<input type="radio" name="answer_3" value="%s">
                       <br>
                       <br>
                       <input type= "submit">
                       </form>
                       <br>
                       <br>
                       </div>
                       <div class="black">
                       This prototype is based on psychological scales published in the following articles:
                        <ul>
                        <li>
                        S. Verheyen and M. Peterson, “Can we use conceptual spaces to model moral principles?,” Rev. Philos. Psychol., vol. 12, no. 2, pp. 373–395, 2021.
                        </li>
                        </ul>
                        </div>
                       <div class=footer-bottom>
                       <br>
                       <br>
                        <br>
                           
                       Kyle Seakgwa(c)
                       <br>
                       <br>
                       <br>
                       </div>
                       </body>
                       </html>"""%(question_id+1,question_text, question_id,csrf_token_html, principles[0],principles[0],principles[1],principles[1],principles[2],principles[2],principles[3],principles[3]))
                       
    except IndexError:
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/results_3/")
    
@csrf_exempt    
def prototype_3_answers(request, question_id):
    
    answer=request.POST["answer_3"]
    
    prototype_3_questions=request.session["prototype_3_questions"]
    
    if answer=='':
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_3/"%(question_id))
    
    request.session["answers"].append(answer)
    request.session.modified= True
    
    principles=["An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost.",
                "An action is right if its ends are in the agent's self-interest",
                "An action is right if God wills it so",
                "An action is right if it is universally willable and it respects the rational autonomy of others." 
               ]
    if prototype_3_questions[question_id]["question_text"]== '"This is a control question to check whether you are paying attention. Please proceed by selecting "An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost." on the scale below."':
        
        if answer==principles[0]:
            
            request.session["attention_check_3"].append("Yes")
            request.session.modified= True
            return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_3/"%(question_id+1))
        else:
           request.session["attention_check_3"].append("No")
           request.session.modified= True
           return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_3/"%(question_id+1))
     
    if answer== principles[0]:

        if prototype_3_questions[question_id]["question_text"]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting "An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost." on the scale below."':
        
            request.session["utilitarianism_score"]+=1
        
            return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_3/"%(question_id+1))
     
    if answer== principles[1]:    
        if prototype_3_questions[question_id]["question_text"]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting "An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost." on the scale below."': 
            request.session["egoism_score"]+=1
        
            return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_3/"%(question_id+1))
    
    if answer== principles[2]:    
        if prototype_3_questions[question_id]["question_text"]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting "An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost." on the scale below."':       
            request.session["dct_score"]+=1
        
            return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_3/"%(question_id+1))
    
    if answer== principles[3]:    
        if prototype_3_questions[question_id]["question_text"]!= '"This is a control question to check whether you are paying attention. Please proceed by selecting "An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost." on the scale below."': 
            request.session["kantianism_score"]+=1
        
            return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/questions_3/"%(question_id+1))
    
@csrf_exempt    
def results_3(request):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
    prototype_3_questions=request.session["prototype_3_questions"]
    if request.session["utilitarianism_score"]>request.session["egoism_score"] and request.session["utilitarianism_score"]>request.session["dct_score"] and request.session["utilitarianism_score"]>request.session["kantianism_score"]:
        
        result= "You are a utilitarian"
    
    elif request.session["egoism_score"]>request.session["utilitarianism_score"] and request.session["egoism_score"]>request.session["dct_score"] and request.session["egoism_score"]>request.session["kantianism_score"]:
        
        result="You are an egoist"
        
    elif request.session["dct_score"]>request.session["utilitarianism_score"] and request.session["dct_score"]>request.session["egoism_score"] and request.session["dct_score"]>request.session["kantianism_score"]:
        
        result="You are a divine command theorist"
        
    elif request.session["kantianism_score"]>request.session["utilitarianism_score"] and request.session["kantianism_score"]>request.session["egoism_score"] and request.session["kantianism_score"]>request.session["dct_score"]:
        
        result="You are a deontologist"
    
    else:

        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/importance_check/")
    
    if "Yes" in request.session["attention_check_3"]:
        
       GenetUsers3.objects.create(user_classification=result,attention_check="Passed",question_1=request.session["questions"][0],answer_1=request.session["answers"][0],question_2=request.session["questions"][1],answer_2=request.session["answers"][1],question_3=request.session["questions"][2],answer_3=request.session["answers"][2],question_4=request.session["questions"][3],answer_4=request.session["answers"][3],question_5=request.session["questions"][4],answer_5=request.session["answers"][4],question_6=request.session["questions"][5],answer_6=request.session["answers"][5],question_7=request.session["questions"][6],answer_7=request.session["answers"][6])

       current_user= GenetUsers3.objects.last()          
    
 
       return HttpResponse("""<html>
                        <style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height: 110px
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                              </style>
                              
                        <head><title>result</title></head>
                        <div class="black">
                        <br>
                        <body><div><h2>Result</h2></div>
                        </div>
                        <div class="content">
                        <br>
                        <p> Please remember the following information (write it down if necessary):</p>
                        <br>
                        <br>
                        <p>%s</p>
                        <br>
                        <p> Your participant number is: %s </p>
                        <br>
                        <p> The prototype you interacted with was: Prototype 3 </p>
                        <br>
                        <form action="https://survey.cs.uct.ac.za/limesurvey/index.php/445565?lang=en">
                        <p>Click the button below to continue to the next part of the study</p>
                        <br>
                        <center><input type="submit" value= "Continue"/></center>
                        </form>
                        <br>
                        </div>
                        <div class="black">
                        This prototype is based on psychological scales published in the following articles:
                        <ul>
                        <li>
                        S. Verheyen and M. Peterson, “Can we use conceptual spaces to model moral principles?,” Rev. Philos. Psychol., vol. 12, no. 2, pp. 373–395, 2021.
                        </li>
                        </ul>
                        <br>
                        </div>
                        <div class= "footer-bottom">
                        
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                        </body>
                        </html>"""%(result, current_user))

       
    
    else:

        GenetUsers3.objects.create(user_classification=result,attention_check="Failed",question_1=request.session["questions"][0],answer_1=request.session["answers"][0],question_2=request.session["questions"][1],answer_2=request.session["answers"][1],question_3=request.session["questions"][2],answer_3=request.session["answers"][2],question_4=request.session["questions"][3],answer_4=request.session["answers"][3],question_5=request.session["questions"][4],answer_5=request.session["answers"][4],question_6=request.session["questions"][5],answer_6=request.session["answers"][5],question_7=request.session["questions"][6],answer_7=request.session["answers"][6])
       
        current_user= GenetUsers3.objects.last()

        return HttpResponse("""<html>
                        <style>
                                H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height: 110px
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center}
                              </style>
                              
                        <head><title>result</title></head>
                        <div class="black">
                        <br>
                        <body><div><h2>Result</h2></div>
                        </div>
                        <div class="content">
                        <br>
                        <br>
                        <br>
                        <br>
                        <p>%s</p>
                        <br>
                        <p> Your participant number is: %s </p>
                        <br>
                        <p> The prototype you interacted with was: Prototype 3 </p>
                        <br>
                        </div>
                        <br>
                        <div class="black">
                        This prototype is based on psychological scales published in the following articles:
                        <ul>
                        <li>
                        S. Verheyen and M. Peterson, “Can we use conceptual spaces to model moral principles?,” Rev. Philos. Psychol., vol. 12, no. 2, pp. 373–395, 2021.
                        </li>
                        </ul>
                        <br>
                        </div>
                        <div class= "footer-bottom">
                        
                       Kyle Seakgwa(c)
                       <br>
                       </div>
                        </body>
                        </html>"""%(result, current_user))

def importance_checker(request):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)
       
    request.session["tie_breaker_score_1"]= 0
    
    request.session["tie_breaker_score_2"]= 0

    request.session["tie_breaker_score_3"]= 0
    
    def list_duplicates_of(seq,item):
    
        start_at = -1
        locs = []
        while True:
            try:
                loc = seq.index(item,start_at+1)
            except ValueError:
                break
            else:
                locs.append(loc)
                start_at = loc
        return locs

    scores= {"util":request.session["utilitarianism_score"],"ego":request.session["egoism_score"], "dct":request.session["dct_score"],"kant": request.session["kantianism_score"] }
    
    highest_score= max(scores, key=scores.get)
    highest_score= scores[highest_score]
    flipped_scores={}
                                    
    
    for key, value in scores.items():
        
        flipped_scores.setdefault(value, set()).add(key)
                                                        
    tied_theories=[]
                                                                
    
    for score in flipped_scores:   
        
        if score == highest_score:       
            
            tied_theories.append(list(flipped_scores[score]))
                                                                                                                        
    possible_answers=["An action is right if out of its alternatives it is the one that increases overall happiness at the smallest emotional cost.",
"An action is right if its ends are in the agent's self-interest",
"An action is right if God wills it so","An action is right if it is universally willable and it respects the rational autonomy of others."]
                                                                                                                                
    
    tie_answers=[]
    
    answer_indices=[]
    

    if "util" in tied_theories[0]:
        

        tie_answers.append(possible_answers[0])
        
        answers= request.session["answers"]

        indices=list_duplicates_of(answers, possible_answers[0])

        answer_indices.append([indices, "util"])

    if "ego" in tied_theories[0]:

        tie_answers.append(possible_answers[1])

        answers= request.session["answers"]

        indices=list_duplicates_of(answers, possible_answers[1])

        answer_indices.append([indices, "ego"])

    if "dct" in tied_theories[0]: 

        tie_answers.append(possible_answers[2])  
        answers= request.session["answers"]
        indices=list_duplicates_of(answers, possible_answers[2])

        answer_indices.append([indices, "dct"])
    if "kant" in tied_theories[0]:
        
        tie_answers.append(possible_answers[3])

        answers= request.session["answers"]
        
        indices=list_duplicates_of(answers, possible_answers[3])

        answer_indices.append([indices, "kant"])
    
    request.session["answer_indices"]= answer_indices
   
    questions= request.session["questions"]  
    
    questions_1= []
    questions_2= []
    questions_3= []
    
    for index_tuple in answer_indices:

        if index_tuple[1]==tied_theories[0][0]:
            for index in index_tuple[0]:
                questions_1.append(questions[index][1:-3])
        
        if index_tuple[1]==tied_theories[0][1]:
            for index in index_tuple[0]:
                questions_2.append(questions[index][1:-3])
        try:
            if index_tuple[1]==tied_theories[0][2]:
                for index in index_tuple[0]:
                    questions_3.append(questions[index][1:-3])
        except:
            continue

    request.session["questions_1"]= questions_1
    request.session["questions_2"]= questions_2
    request.session["questions_3"]= questions_3
    request.session["tied_theories"]= tied_theories 
    
    return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/0/tie_breaker_display/")

def tie_breaker_display(request, display_index):
    
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)

    questions_1 = request.session["questions_1"]
    
    questions_2 = request.session["questions_2"]
    
    questions_3 = request.session["questions_3"]
    
    tied_theories = request.session["tied_theories"]

    if 'This is a control question to check whether you are paying attention. Please proceed by selecting utilitarianism on the scale below' in questions_1:
        
        questions_1.remove('This is a control question to check whether you are paying attention. Please proceed by selecting utilitarianism on the scale below')
    
    if 'This is a control question to check whether you are paying attention. Please proceed by selecting utilitarianism on the scale below' in questions_2:
        
        questions_2.remove('This is a control question to check whether you are paying attention. Please proceed by selecting utilitarianism on the scale below')
    
    try:
        if 'This is a control question to check whether you are paying attention. Please proceed by selecting utilitarianism on the scale below' in questions_3:
            
            questions_3.remove('This is a control question to check whether you are paying attention. Please proceed by selecting utilitarianism on the scale below')
    except:
        pass

    if len(tied_theories[0])==2:
        try:
            return HttpResponse("""<html>
        <style> 
                             H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height: 110px;
                                width: 100%%
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center}

                </style>
                <head><title>Prototype 3</title></head> 
                <body>  
                <div class=black>
                <br>
                <h2>Prototype 3</h2>
                </div>
                <div class=content>
                <h3>%s of %s</h3>

                <body>
                <p>Which of the following 2 scenarios presents the most important decision</p>                                    
<br>

<form method= "post" action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/tie_breaker_answers/">
%s
<br>
%s <input type="radio" name= "tie_answer" value= "%s" >
<br>
<br>
%s <input type="radio" name= "tie_answer" value= "%s" >
<br>                                                                                                                                    
<br>
<br>
<input type= "submit">
</form>
</div>
<br>
<div class="black">
This prototype is based on psychological scales published in the following articles:
<ul>                                                                                                                                                                   
<li>
S. Verheyen and M. Peterson, Can we use conceptual spaces to model moral principles?, Rev. Philos. Psychol., vol. 12, no. 2, pp. 373395, 2021.
</li>
</ul>
</div>
<div class=footer-bottom>                                                                                                                
<br>
Kyle Seakgwa(c)
<br>
<br>
<br>
</div>
</body>
</html>"""%(display_index+1, len(questions_1), display_index, csrf_token_html, questions_1[display_index],questions_1[display_index], questions_2[display_index],questions_2[display_index]))

        except IndexError:        
        
            return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/tie_breaker_results/")

    elif len(tied_theories[0])==3:
        
        try:
            return HttpResponse("""<html>
        <style> 
        H2 {text-align: center}
                                H3 {font-family:"arial";
                                        text-align:center;
                                }
                                P {font-family:"arial";
                                text-align:center;
                                }
                                div.content{min-height:100%%}
                                div.black{font-family:"arial";
                                background: black;
                                color: white;
                                height: 110px;
                                width:100%%
                                }
                                div.footer-bottom{
                                font-family:"arial";
                                background: black;
                                color: white;
                                height:75px;
                                width:100%%;
                                position:absolute;
                                text-align: center}

                </style>
                <head><title>Prototype 3</title></head> 
                <body>  
                <div class=black>
                <br>
                <h2>Prototype 3</h2>
                </div>
                <div class=content>
                <h3>%s of %s</h3>

                <body>
                <p>Which of the following 2 scenarios presents the most important decision</p>                                    
<br>

<form method= "post" action="https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/tie_breaker_answers/">
%s
<br>
%s <input type="radio" name= "tie_answer" value= "%s" >
<br>
<br>
%s <input type="radio" name= "tie_answer" value= "%s" >
<br>                                                                                                                                    
<br>
%s <input type="radio" name= "tie_answer" value= "%s" >
<br>
<br>
<input type= "submit">
</form>
<br>
</div>
<br>
<div class="black">
This prototype is based on psychological scales published in the following articles:
<ul>                                                                                                                                                                   
<li>
S. Verheyen and M. Peterson, Can we use conceptual spaces to model moral principles?, Rev. Philos. Psychol., vol. 12, no. 2, pp. 373395, 2021.
</li>
</ul>
</div>
<div class=footer-bottom>                                                                                                                
<br>
Kyle Seakgwa(c)
<br>
<br>
<br>
</div>
</body>
</html>"""%(display_index+1, len(questions_1), display_index, csrf_token_html, questions_1[display_index],questions_1[display_index], questions_2[display_index],questions_2[display_index],questions_3[display_index],questions_3[display_index]))

        except IndexError:        
        
            return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/tie_breaker_results/")



@csrf_exempt
def tie_breaker_answers(request, display_index):

    answer = request.POST.get("tie_answer") 
    
    questions_1 = request.session["questions_1"]

    questions_2 = request.session["questions_2"]
    
    questions_3=request.session["questions_3"]

    if answer=="":
        
        return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/tie_breaker_answers/")
    
    if answer in questions_1:
    
        request.session["tie_breaker_score_1"]+=1
        
        request.session.modified= True
    
    if answer in questions_2:
        
        request.session["tie_breaker_score_2"]+=1
            
        request.session.modified= True
    
    if answer in questions_3:
        
        request.session["tie_breaker_score_3"]+=1

        request.session.modified= True
    
    display_index+=1

    return HttpResponseRedirect("https://genetelicitationtool.cs.uct.ac.za/Genet_prototypes/%s/tie_breaker_display/"%(display_index))

@csrf_exempt
def tie_breaker_results(request): 

    csrf_token = get_token(request)

    answer_indices=request.session["answer_indices"]

    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" >'.format(csrf_token)

    questions=request.session["questions"]

    questions_1 = request.session["questions_1"]
    
    questions_2 = request.session["questions_2"]
    questions_3 = request.session["questions_3"] 
    tied_theories=request.session["tied_theories"]

    if len(tied_theories[0])==2:
        
        if request.session["tie_breaker_score_1"]>request.session["tie_breaker_score_2"]:
        
            theory= tied_theories[0][0]

        if request.session["tie_breaker_score_1"]<request.session["tie_breaker_score_2"]:

            theory= tied_theories[0][1]
    
    elif len(tied_theories[0])==3:
        
        tied_scores=[request.session["tie_breaker_score_1"],request.session["tie_breaker_score_2"],request.session["tie_breaker_score_3"]]
        
        if max(tied_scores)==request.session["tie_breaker_score_1"]:
    
            theory= tied_theories[0][0]
        
        if max(tied_scores)==request.session["tie_breaker_score_2"]:
            
            theory= tied_theories[0][1]
        
        if max(tied_scores)==request.session["tie_breaker_score_3"]:
            
            theory= tied_theories[0][2]
    try:
        
        if theory == "util":
            
            result= "You are a utilitarian"

        if theory == "dct": 

            result= "You are a divine command theorist"

        if theory == "ego":

            result= "You are an egoist"

        if theory == "kant":

            result= "You are a deontologist"

    except KeyError:
       
        result= "Your moral theory is not ascertainable by Genet at this time"       
    
    if "Yes" in request.session["attention_check_3"]:
       
        GenetUsers3.objects.create(user_classification=result,attention_check="Passed",question_1=request.session["questions"][0],answer_1=request.session["answers"][0],question_2=request.session["questions"][1],answer_2=request.session["answers"][1],question_3=request.session["questions"][2],answer_3=request.session["answers"][2],question_4=request.session["questions"][3],answer_4=request.session["answers"][3],question_5=request.session["questions"][4],answer_5=request.session["answers"][4],question_6=request.session["questions"][5],answer_6=request.session["answers"][5],question_7=request.session["questions"][6],answer_7=request.session["answers"][6])

        current_user= GenetUsers3.objects.last()

        return HttpResponse("""<html>                                                                                                                                                                  <style>
                             H2 {text-align: center}
                             H3 {font-family:"arial";
                                     text-align:center;
                             }
                             P {font-family:"arial";
                             text-align:center;
                             }
                             div.content{min-height:100%%}
                             div.black{font-family:"arial";
                              background: black;
                              color: white;
                              height: 110px
                              }
                              div.footer-bottom{
                              font-family:"arial";
                              background: black;
                              color: white;
                              height:75px;
                              width:100%%;
                              position:absolute;
                              text-align: center}
                              </style>
                             <head><title>result</title></head>
                             <div class="black">
                             <br>
                             <body><div><h2>Result</h2></div>
                             </div>
                             <div class="content">
                             <br>
<br>
<br>
<br>
<br>
<p>%s</p>
<br>
<br>
<br>
<p> Your participant number is: %s </p>
<br> 
<center><a href="https://survey.cs.uct.ac.za/limesurvey/index.php/445565?lang=en">Click here to continue the next part of the study</a><center>


</div>
<br>
<div class="black">
This prototype is based on psychological scales published in the following articles:
<ul>
<li>
S. Verheyen and M. Peterson, “Can we use conceptual spaces to model moral principles?,” Rev. Philos. Psychol., vol. 12, no. 2, pp. 373–395, 2021.
 </li>
 </ul>
 <br>
 </div>
 <div class= "footer-bottom">
 
Kyle Seakgwa(c)
<br>
</div>
 </body>
 </html>"""%(result, current_user))

    else:
        GenetUsers3.objects.create(user_classification=result,attention_check="Failed",question_1=request.session["questions"][0],answer_1=request.session["answers"][0],question_2=request.session["questions"][1],answer_2=request.session["answers"][1],question_3=request.session["questions"][2],answer_3=request.session["answers"][2],question_4=request.session["questions"][3],answer_4=request.session["answers"][3],question_5=request.session["questions"][4],answer_5=request.session["answers"][4],question_6=request.session["questions"][5],answer_6=request.session["answers"][5],question_7=request.session["questions"][6],answer_7=request.session["answers"][6])
        
        current_user= GenetUsers3.objects.last()
        
        return HttpResponse("""<html>
                           <style>
                                   H2 {text-align: center}
                                   H3 {font-family:"arial";
                                           text-align:center;
                                   }
                                   P {font-family:"arial";
                                   text-align:center;
                                   }
                                   div.content{min-height:100%%}
                                   div.black{font-family:"arial";
                                   background: black;
                                   color: white;
                                   height: 110px;
                                   width:100%%;
                                   }
                                   div.footer-bottom{
                                   font-family:"arial";
                                   background: black;
                                   color: white;
                                            height:75px;
                                            width:100%%;
                                            position:absolute;
                                            text-align: center}
                                            </style>
                                           <head><title>result</title></head>
                                            <div class="black">
                                            <br>
                                            <body><div><h2>Result</h2></div>
                                            </div>
                                            <div class="content">
                                                                      <br>
<br>
<br>
<br>
<br>
<p>%s</p>
<br>
<br>
<br>
<p> Your participant number is: %s </p>
<br> 
<br>

</div>
<br>
<div class="black">
This prototype is based on psychological scales published in the following articles:
<ul>
<li>
S. Verheyen and M. Peterson, “Can we use conceptual spaces to model moral principles?,” Rev. Philos. Psychol., vol. 12, no. 2, pp. 373–395, 2021.
</li>
</ul>
<br>
</div>
<div class= "footer-bottom">
 
Kyle Seakgwa(c)
<br>
</div>
 </body>
 </html>"""%(result, current_user))


