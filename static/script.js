$(document).ready(function () {
    $("#product-item").autocomplete({
        source: dataItemList.map((x) => x.product_name),
        select: function (event, ui) {
            $(this).val("");
            let item = dataItemList.find((e) => e.product_name === ui.item.value)
            $(".product-list").prepend(`<li class="list-group-item d-flex justify-content-between lh-condensed">
                                            <div>
                                                <h6 class="my-0">${item.product_name.substring(0, item.product_name.length - 12)}</h6>
                                                <small class="text-muted">${item.product_name.substring(item.product_name.length - 12, item.product_name.length)}</small>
                                            </div>
                                            <span class="text-muted price">${item.product_price}</span>
                                        </li>`)
            let subTotal = 0
            $(".price").toArray().forEach(element => {
                subTotal += parseInt($(element).text().replaceAll(".", ""))
            });
            $("#sub-total").text(new Intl.NumberFormat("en-DE").format(subTotal))
            calcTotal();
            return false;
        }
    })
        .autocomplete("instance")._renderItem = function (ul, item) {
            $(ul).addClass("dropdown-menu")
            return $("<li>")
                .append(`<pre><a class="dropdown-item" href="#">${item.label}</a></pre>`)
                .appendTo(ul);
        };;
    $("#tax").on("change", (e) => {
        calcTotal();
    })

    $(document).on("ajaxSend", function () { blockUI() }).on("ajaxComplete", function () { $.unblockUI(); });
});

function calcTotal() {
    let subTotal = parseInt($("#sub-total").text().replaceAll(".", ""));
    let tax = parseFloat($("#tax").val())
    if (!isNaN(tax)) {
        let total = isNaN(subTotal) ? "" : new Intl.NumberFormat("en-DE").format(subTotal * tax + subTotal);
        $("#total").text(total)
    }
}

function exportInvoice() {

    let data = {
        "invoice_date": new Date().toLocaleString(),
        "invoice_num": Math.floor(Math.random() * 10001),
        "product_name": "Abc",
        "bank_num": "123-456-789",
        "bank_account_name": "ABC Company",
        "bank_name": "VCB",
        "customer_name": `${$("#firstName").val()} ${$("#lastName").val()}`,
        "customer_address": $("#address").val(),
        "terms_conditions": "abc",
        "item": [
        ],
        "sub_total": $("#sub-total").text(),
        "tax": $("#tax").val(),
        "total": $("#total").text(),
    }

    $.ajax({
        type: "POST",
        url: "/export",
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: "json",
    })
        .always(function (res) {
            if (res.status === 200) {
                let pdfWindow = window.open("")
                pdfWindow.document.write(
                    `<iframe width="100%" height="100%" src="data:application/pdf;base64,${encodeURI(res.responseText)}"></iframe>`
                )
            }
        });
}

function blockUI() {
    $.blockUI({
        css: {
            backgroundColor: 'transparent',
            border: 'none'
        },
        message: '<div class="lds-ring"><div></div><div></div><div></div><div></div></div>',
        overlayCSS: {
            backgroundColor: '##f7f7f7',
            opacity: 0.7,
            cursor: 'wait'
        }
    });
}

var dataItemList = [
    {
        "id": 1,
        "product_img": "lenovo-v15-g3-iap-i5-82tt0064vn-glr-a-2.jpg",
        "product_name": "Laptop Lenovo V15 G3 IAP i5 1235U/8GB/512GB/Win11 (82TT0064VN)",
        "product_price": "14.390.000"
    },
    {
        "id": 2,
        "product_img": "lenovo-thinkbook-14-g4-iap-i5-21dh00b5vn-ab-2.jpg",
        "product_name": "Laptop Lenovo ThinkBook 14 G4 IAP i5 1240P/8GB/512GB/Win11 (21DH00B5VN)",
        "product_price": "19.190.000"
    },
    {
        "id": 3,
        "product_img": "lenovo-yoga-slim-7-carbon-13itl5-i5-82nh00avvn-xy-2.jpg",
        "product_name": "Laptop Lenovo Yoga Slim 7 Carbon 13ITL5 i5 1135G7/16GB/512GB/Win11 (82EV00AVVN)",
        "product_price": "20.190.000"
    },
    {
        "id": 4,
        "product_img": "lenovo-yoga-7-14ial7-i5-82qe000rvn-a-2.jpg",
        "product_name": "Laptop Lenovo Yoga 7 14IAL7 i5 1240P/16GB/512GB/Touch/Pen/Win11 (82QE000RVN)",
        "product_price": "21.590.000"
    },
    {
        "id": 5,
        "product_img": "lenovo-yoga-slim-7-carbon-13itl5-i7-82ev00awvn-2.jpg",
        "product_name": "Laptop Lenovo Yoga Slim 7 Carbon 13ITL5 i7 1165G7/16GB/1TB/Win11 (82EV00AWVN)",
        "product_price": "24.390.000"
    },
    {
        "id": 6,
        "product_img": "lenovo-thinkbook-15-g5-irl-i7-121jd002avn-1.jpg",
        "product_name": "Laptop Lenovo ThinkBook 15 G5 IRL i7 1355U/16GB/512GB/15.6/Win11 (21JD002AVN)",
        "product_price": "25.990.000"
    },
    {
        "id": 7,
        "product_img": "lenovo-yoga-duet-7-13itl6-i5-82ma009nvn-2-1.jpg",
        "product_name": "Laptop Lenovo Yoga Duet 7 13ITL6 i5 1135G7/8GB/512GB/Touch/Pen/Win11 (82MA009NVN)",
        "product_price": "27.790.000"
    },
    {
        "id": 8,
        "product_img": "lenovo-thinkpad-p16s-gen-1-i7-21bt0064vn-glr-2.jpg",
        "product_name": "Laptop Lenovo Thinkpad P16s Gen 1 i7 1260P/16GB/512GB/4GB QuadroT550/Win11 Pro (21BT0064VN)",
        "product_price": "44.490.000"
    },
    {
        "id": 9,
        "product_img": "lenovo-ideapad-5-pro-14iap7-i5-82sh000svn-a-2.jpg",
        "product_name": "Laptop Lenovo Ideapad 5 Pro 14IAP7 i5 1240P/16GB/512GB/Win11 (82SH000SVN)",
        "product_price": "19.990.000"
    },
    {
        "id": 10,
        "product_img": "lenovo-ideapad-5-15ial7-i5-82sf005hvn-glr-2.jpg",
        "product_name": "Laptop Lenovo Ideapad 5 15IAL7 i5 1235U/8GB/512GB/Win11 (82SF005HVN)",
        "product_price": "16.990.000"
    },
    {
        "id": 11,
        "product_img": "",
        "product_name": "Mouse Fuhlen G90 Black",
        "product_price": "290.000"
    },
    {
        "id": 12,
        "product_img": "",
        "product_name": "Headphone Asus ROG STRIX GO 2.4",
        "product_price": "2.990.000"
    }
]