import yaml
import re

# Read the publications data
with open('_data/publications.yml', 'r') as f:
    publications = yaml.safe_load(f)

def format_authors(authors_string):
    """Format authors with commas and 'and' before the last name, bold Ahmed H Elsayed"""
    # Split by 'and' to get individual authors
    authors = re.split(r'\s+and\s+', authors_string)
    
    # Bold Ahmed H Elsayed (with or without periods)
    formatted_authors = []
    for author in authors:
        if 'Ahmed H Elsayed' in author or 'Ahmed H. Elsayed' in author:
            author = f'<strong>{author}</strong>'
        formatted_authors.append(author)
    
    # Join with commas and 'and' before the last
    if len(formatted_authors) == 1:
        return formatted_authors[0]
    elif len(formatted_authors) == 2:
        return f'{formatted_authors[0]} and {formatted_authors[1]}'
    else:
        return ', '.join(formatted_authors[:-1]) + f', and {formatted_authors[-1]}'

# Image mapping for publications
# Add your image files to images/publications/ folder
# Then add the mapping here with the exact publication title as the key
images = {
    'Design and control of soft biomimetic pangasius fish robot using fin ray effect and reinforcement learning': 
        'images/publications/pangasius_paper.png',
    'UJI-Butler: A Symbolic/Non-symbolic Robotic System that Learns Through Multi-modal Interaction':
        'images/publications/uji_butler.png',
    'Interactive Simulator Framework for XAI Applications in Aquatic Environments':
        'images/publications/Interactive_Simulator_Framework.png',
    'Human-Robot Collaboration System Setup for Weed Harvesting Scenarios in Aquatic Lakes':
        'images/publications/Human-Robot_Collaboration.jpg',
}

# Generate HTML for publications
html_content = ''
for pub in publications:
    title = pub['title']
    authors_formatted = format_authors(pub['authors'])
    
    # Check if this publication has an image
    image_html = ''
    if title in images:
        image_html = f'<img class="publication-img" src="{images[title]}" alt="{title}">'
    
    html_content += f'''                <div class="publication fade-in">
                    <h3 class="publication-title">{title}</h3>
                    <div class="publication-details">
                        {image_html}
                        <div class="citation">
                            <p>{authors_formatted} ({pub['year']}).</p>
                            <p><i>{pub['venue']}</i></p>
                            <p><a href="{pub['link']}" target="_blank" style="color: var(--text-color); font-weight: bold;">View Publication →</a></p>
                        </div>
                    </div>
                </div>
'''

# Read the current publications.html
with open('publications.html', 'r') as f:
    content = f.read()

# Replace the publications container content
start_marker = '<div id="publications-container">'
end_marker = '</section>'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_content = (
        content[:start_idx + len(start_marker)] +
        '\n' + html_content +
        '            ' + content[end_idx:]
    )
    
    # Write the updated content
    with open('publications.html', 'w') as f:
        f.write(new_content)
    
    print("Successfully updated publications.html with all publications!")
else:
    print("Could not find markers in publications.html")
