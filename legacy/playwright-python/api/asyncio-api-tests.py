import asyncio
from playwright.async_api import async_playwright

async def api_testing():
    async with async_playwright() as p:
        # Create a new browser context
        browser = await p.chromium.launch()
        context = await browser.new_context()

        # Create a new request context
        request_context = await context.new_request()

        # Example GET request
        response = await request_context.get('https://jsonplaceholder.typicode.com/posts/1')
        print(f'Status Code: {response.status}')
        print(f'Response Body: {await response.json()}')

        # Validate the response
        assert response.status == 200
        response_body = await response.json()
        assert response_body['id'] == 1

        # Example POST request
        post_data = {
            'title': 'foo',
            'body': 'bar',
            'userId': 1
        }
        response = await request_context.post('https://jsonplaceholder.typicode.com/posts', data=post_data)
        print(f'Status Code: {response.status}')
        print(f'Response Body: {await response.json()}')

        # Validate the response
        assert response.status == 201
        response_body = await response.json()
        assert response_body['title'] == 'foo'

        # Close the browser context
        await context.close()
        await browser.close()

# Run the API testing function
asyncio.run(api_testing())
