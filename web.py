# The MIT License (MIT)

#Copyright © Carmen Plaza Seco

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import http.server
import http.client
import json
import socketserver

class OpenFDAClient():

    OPENFDA_API_URL="api.fda.gov"
    OPENFDA_API_EVENT="/drug/event.json"
    OPENFDA_API_DRUG='&search=patient.drug.medicinalproduct:'
    OPENFDA_API_COMPANY='&search=companynumb:'
    OPENFDA_API_PATIENTSEX='/patient/patientsex:'

    def get_event(self,number_limit):
        #GET EVENT
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=" + number_limit)
        r1 = conn.getresponse()
        data1 = r1.read()
        data=data1.decode("utf8")
        biblioteca_data=json.loads(data)
        events= biblioteca_data['results']
        return events

    def get_event_search_drug(self, drug_search):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10"+ self.OPENFDA_API_DRUG + drug_search)
        r1 = conn.getresponse()
        data1 = r1.read()
        data=data1.decode("utf8")
        biblioteca_data=json.loads(data)
        events_search_drug= biblioteca_data['results']
        return events_search_drug

    def get_event_search_company(self, company_search):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10"+ self.OPENFDA_API_COMPANY + company_search)
        r1 = conn.getresponse()
        data1 = r1.read()
        data=data1.decode("utf8")
        biblioteca_data=json.loads(data)
        events_search_company= biblioteca_data['results']
        return events_search_company

    def get_events_patientsex(self, number_limit):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=" + number_limit + self.OPENFDA_API_PATIENTSEX )
        r1 = conn.getresponse()
        data1 = r1.read()
        data=data1.decode("utf8")
        biblioteca_data=json.loads(data)
        events_patientsex= biblioteca_data['results']
        return events_patientsex


class OpenFDAParser():

    def get_drugs(self,events):
        drugs=[]
        for event in events:
            drugs+= [event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_companies(self,events):
        companies=[]
        for event in events:
            companies+= [event['companynumb']]
        return companies

    def get_companies_from_drug(self,events_search_drug):
        companies=[]
        for event in events_search_drug:
            companies+=[event['companynumb']]
        return companies

    def get_drugs_from_company(self, events_search_company):
        drugs=[]
        for event in events_search_company:
            drugs+=[event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_patientsex(self,events_patientsex):
        patientsex=[]
        for event in events_patientsex:
            patientsex+= [event['patient']['patientsex']]
        return patientsex


class OpenFDAHTML():

    def html_error_404(self):
        html_error="""
            <html>
                <head>
                    <title>Error Not Found</title>
                    <h1>ERROR NOT FOUND</h1>
                </head>
                    <body>The requested resource could not be found but may be available in the future. Subsequent requests by the client are permissible</body>
        """
        return html_error

    def get_main_page(self):
        html = """
            <html>
                <head>
                    <title>OpenFDA Cool App</title>
                </head>
                <body>
                    <h1>OpenFDA Client </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        <body> Limit number </body>
                        <input type = "text" size="3" name="limit"></input>
                        </input>
                    </form>
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        <body> Limit number </body>
                        <input type = "text" size="3" name="limit"></input>
                        </input>
                    </form>
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    <form method="get" action="listGender">
                        <input type = "submit" value="Patient sex">
                        <body> Limit number </body>
                        <input type = "text" size="3" name="limit"></input>
                        </input>
                    </form>
                </body>
            </html>
                """
        return html

    def get_second_page(self, items):
        list_html = """
            <html>
                <head>
                    <title>OpenFDA Cool App</title>
                </head>
                <body>
                    <ol>
        """
        for item in items:
            list_html+="<li>"+item+"</li>"

        list_html += """
                    </ol>
                </body>
            </html>
        """
        return list_html

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET

    def do_GET(self):

        FOUND=200

        client =OpenFDAClient()
        logic =OpenFDAParser()
        html=OpenFDAHTML()

        if self.path=='/':
            html=html.get_main_page()


        elif 'listDrugs' in self.path:
            if len(self.path.split('=')) == 1:
                limit='10'
            else:
                limit=self.path.split('=')[1]
            event=client.get_event(limit)
            drugs=logic.get_drugs(event)
            html=html.get_second_page(drugs)


        elif 'listCompanies' in self.path:
            if len(self.path.split('=')) == 1:
                limit='10'
            else:
                limit=self.path.split('=')[1]
            event=client.get_event(limit)
            companies=logic.get_companies(event)
            html=html.get_second_page(companies)


        elif 'searchDrug' in self.path:
            drug=self.path.split('=')[1]
            event=client.get_event_search_drug(drug)
            companies=logic.get_companies_from_drug(event)
            html=html.get_second_page(companies)


        elif  'searchCompany' in self.path:
            company=self.path.split('=')[1]
            event=client.get_event_search_company(company)
            companies=logic.get_drugs_from_company(event)
            html=html.get_second_page(companies)


        elif 'listGender' in self.path:
            if len(self.path.split('=')) == 1:
                limit='10'
            else:
                limit=self.path.split('=')[1]
            event=client.get_events_patientsex(limit)
            patientsex=logic.get_patientsex(event)
            html=html.get_second_page(patientsex)

        elif '/redirect' in self.path:
            self.send_response(302)
            self.send_header('Location','/')
            self.end_headers()

        elif '/secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate','Basic realm= "My realm"')
            self.end_headers()

        else:
            FOUND=404
            html=html.html_error_404()

        self.send_response(FOUND)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if not '/redirect' in self.path and not '/secret' in self.path:
            self.wfile.write(bytes(html, "utf8"))


        return
