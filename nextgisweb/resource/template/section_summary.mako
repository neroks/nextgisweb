<%! from nextgisweb.resource.util import _ %>
<table class="pure-table pure-table-vertical" style="margin-bottom: 1em"><tbody>
    <tr>
        <th>${tr(_("Display name"))}</th>
        <td>${obj.display_name}</td>
    </tr>

    %if obj.keyname:
    <tr>
        <th>${tr(_("Keyname"))}</th>
        <td>${obj.keyname}</td>
    </tr>
    %endif

    <tr>
        <th>${tr(_("Type"))}</th>
        <td>${tr(obj.cls_display_name)} (${obj.cls})</td>
    </tr>

    <tr>
        <th>${tr(_("Owner"))}</th>
        <td>${obj.owner_user}</td>
    </tr>
</tbody></table>