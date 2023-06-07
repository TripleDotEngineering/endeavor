### Risk Assessment

<?ev for risk in risks|sort(attribute='score', reverse=True) ?>

#### ${{ risk['id'] }} ${{ risk.get('short_name', '') }}${{ risk.get('label', '') }}
${{ risk['text'] }}

> **Likelihood:** ${{ risk['likelihood'] }}
>
> **Consequence:** ${{ risk['consequence'] }}
>
> **Score:** ${{ risk['score'] }}
>
<?ev if risk['mitigation'] ?>
> **Mitigation Strategy:** ${{ risk['mitigation'] }}
<?ev endif ?>

<?ev endfor ?>
