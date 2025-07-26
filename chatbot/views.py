from django.shortcuts import render
from django.http import JsonResponse
from .nlp_engine import extract_intent_and_entities
from .query_engine import handle_query as process_query  # ⬅️ Import the query handler

def index(request):
    return render(request, 'index.html')

def handle_query(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')

        # Step 1: Extract intent and entities using NLP engine
        intent, entities = extract_intent_and_entities(query)

        # Step 2: Delegate response generation to query_engine.py
        response = process_query(intent, entities)

        return JsonResponse({'response': response})
