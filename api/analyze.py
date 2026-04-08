import json
import os
import anthropic

def handler(request):
    body = json.loads(request.body)
    hook = body.get("hook")

    score = {
        "watch_signal": len(hook) > 40,
        "emotional_trigger": any(word in hook.lower() for word in ["secret", "shocking", "crazy", "never"]),
        "curiosity_gap": "?" in hook or "..." in hook,
        "retention": len(hook.split()) < 15,
        "clarity": True
    }

    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        messages=[{"role": "user", "content": f"Rewrite this hook in 5 viral ways: {hook}"}]
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "scores": score,
            "rewrites": response.content[0].text
        })
    }
