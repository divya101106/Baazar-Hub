def check_spam_score(title, description):
    """
    Calculate spam score based on heuristics.
    Returns an integer between 0 and 100.
    """
    score = 0
    
    # Heuristic 1: Length check
    if len(title) < 10:
        score += 20
    if len(description) < 50:
        score += 20
        
    # Heuristic 2: Keyword check (basic)
    spam_keywords = ['cash only', 'urgent', 'wire transfer', 'western union']
    text = (title + " " + description).lower()
    for keyword in spam_keywords:
        if keyword in text:
            score += 30
            
    return min(score, 100)

def validate_image(image):
    """
    Validate image content (stub).
    Returns True if safe, False otherwise.
    """
    # In a real app, use Pillow or an external API to check for NSFW content.
    if not image:
        return False
    return True

def should_moderate(spam_score):
    """
    Decide if listing needs manual moderation.
    """
    return spam_score >= 50
