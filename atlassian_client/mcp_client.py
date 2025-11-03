class AtlassianMCPClient:
    """
    Atlassian MCP stub.
    When Atlassian open MCP API, will be instead of REST-client.
    """
    def __init__(self, oauth_token):
        self.token = oauth_token

    def get_context(self, entity_id):
        """Get epic/story/bug context"""
        # Todo: create MCP Context Fetch
        raise NotImplementedError("MCP API is not active yet")

    def create_xray_test(self, test_data):
        """Creation of Xray test case by MCP (further solution)"""
        raise NotImplementedError("MCP API is not active yet")
