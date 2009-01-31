class TextTrackback( TestCase ):
    fixtures = ["test/auth", "test/pingback"]

    def setUp(self):
        self.post = get_test_post()
        self.trackback_url = reverse( "turbion.pingback.views.trackback",
                                      kwargs = { "model" : "blogs.post","id":self.post.id } )

    def test_good_request(self):
        response = self.client.post( self.trackback_url, { "url" : "http://foobar.com/entry/foo/" } )
        self.assertEqual( response.status_code, 200 )

        self.assertEqual( models.Incoming.objects.count(), 1 )
        incoming = models.Incoming.objects.get()

        self.assertEqual( incoming.status, "done" )

        self.assertEqual( incoming.target_url, "http://testserver" + self.trackback_url )
        self.assertEqual( incoming.source_url, "http://foobar.com/entry/foo/" )
