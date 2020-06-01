# emailer
A Google Cloud Function that listens to new files created on a bucket and emails them out using SendGrid.

It uses the following metadata on the file for the email:

| Key        | Extra                                  | Description                                                                      |
|------------|----------------------------------------|----------------------------------------------------------------------------------|
| from       | Defaults to `no-reply@***.com`         | The address the email is from                                                    |
| to         | Required                               | List of address to deliver the file to separated by a semi-colon (`;`)           |
| subject    | Defaults to `MTB Report`               | The email subject                                                                |
| text       | Required                               | Plain email text                                                                 |
| html       | Required                               | HTML / rich email text                                                           |
| categories | Always add `emailer` & current version | List of SendGrid categories to add to the email separated by a semi-colon (`;`). |

Nothing is send when no meta-data is present.

## Environment Variables
See `.env.sample` for those needed by the tests.

## Secrets
A secret is needed in Secret Manager to authenticate with SendGrid:

- sendgrid-api-key