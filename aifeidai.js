/*
 * 这是一张 JavaScript 代码草稿纸。
 *
 * 输入一些 JavaScript，然后可点击右键或从“执行”菜单中选择：
 * 1. 运行 对选中的文本求值(eval) (Ctrl+R)；
 * 2. 查看 对返回值使用对象查看器 (Ctrl+I)；
 * 3. 显示 在选中内容后面以注释的形式插入返回的结果。 (Ctrl+L)
 */
$(function () {
  $('#btnAdd').click(function () {
    $('.ErrorShow').hide();
    var C = $('#txtIDCardNO').val();
    var I = $('#txtMobile').val();
    var H = $('#txtCustomerName').val();
    var A = $('#txtRemark').val();
    var F = $('#hdnVindicatorID').val();
    var E = $('#logonGuid').val();
    var D = $('#ApplyIDCardVerify').val();
    var B = $('#ApplyMobileVerify').val();
    if (C == '') {
      if (D == '1') {
        $('#IDCardError').html(errorImageUrl).show();
        $('#dialog:ui-dialog').dialog('destroy');
        $('#DataNotFound').html('<p>请录入身份证号</p>');
        $('#DataNotFound').dialog({
          modal: true,
          buttons: {
            关闭: function () {
              $(this).dialog('close')
            }
          }
        });
        return false
      } else {
        $('#IDCardError').hide()
      }
    } else {
      if (!isIdCardNo(C)) {
        $('#IDCardError').html(errorImageUrl).show();
        $('#dialog:ui-dialog').dialog('destroy');
        $('#DataNotFound').html('<p>请录入有效客户身份证号</p>');
        $('#DataNotFound').dialog({
          modal: true,
          buttons: {
            关闭: function () {
              $(this).dialog('close')
            }
          }
        });
        return false
      } else {
        $('#IDCardError').hide()
      }
    }
    if (I == '') {
      if (B == '1') {
        $('#MobileError').html(errorImageUrl).show();
        $('#dialog:ui-dialog').dialog('destroy');
        $('#DataNotFound').html('<p>请录入手机号码</p>');
        $('#DataNotFound').dialog({
          modal: true,
          buttons: {
            关闭: function () {
              $(this).dialog('close')
            }
          }
        })
      }
      return false
    } else {
      if (!mobileVal(I)) {
        $('#MobileError').html(errorImageUrl).show();
        $('#dialog:ui-dialog').dialog('destroy');
        $('#DataNotFound').html('<p>手机号码录入有错误</p>');
        $('#DataNotFound').dialog({
          modal: true,
          buttons: {
            关闭: function () {
              $(this).dialog('close')
            }
          }
        });
        return false
      } else {
        $('#MobileError').hide()
      }
    }
    if (H == '') {
      $('#userNameError').html(errorImageUrl).show();
      $('#dialogAgentInfo').dialog('close');
      $('#dialog:ui-dialog').dialog('destroy');
      $('#DataNotFound').html('<p>请录入客户姓名!</p>');
      $('#DataNotFound').dialog({
        modal: true,
        buttons: {
          关闭: function () {
            $(this).dialog('close')
          }
        }
      });
      return false
    } else {
      $('#userNameError').hide()
    }
    var G = /^[\u4E00-\u9FA5]{2,4}$/;
    if (!G.test(H)) {
      $('#userNameError').html(errorImageUrl).show();
      $('#dialog:ui-dialog').dialog('destroy');
      $('#DataNotFound').html('<p>姓名由2-4位中文组成！</p>');
      $('#DataNotFound').dialog({
        modal: true,
        buttons: {
          关闭: function () {
            $(this).dialog('close')
          }
        }
      });
      return
    } else {
      $('#userNameError').hide()
    }
    if (C != '') {
      window.parent.block_viewport();
      IDCardVerify(C, I, H, A, F, E)
    } else {
      window.parent.block_viewport();
      MobileVerify(C, I, H, A, F, E)
    }
  });
  $('#btnHistoryData').click(function () {
    window.parent.GetRecommendBillData()
  });
  $('#btnContinuance').click(function () {
    $('#txtMobile').val('');
    $('#txtCustomerName').val('');
    $('#txtRemark').val('');
    $('#txtIDCardNO').val('');
    $('#applySuccess').hide();
    $('#inputData').show();
    $('.ErrorShow').hide()
  })
});
function IDCardVerify(E, A, B, C, F, D) {
  $.ajax({
    type: 'POST',
    url: recommendCheckProxyBillUrl,
    data: {
      CustomerName: B,
      IDCardNO: E,
      LogonGuid: D,
      Mobile: A,
      BillType: 'A'
    },
    dataType: 'text',
    success: function (H) {
      var G = H.split('&');
      if (H != '') {
        if (G[0] == '1') {
          $.ajax({
            type: 'POST',
            url: getUserAreaLockCheckUrl,
            data: {
              Mobile: A,
              LogonGuid: D
            },
            dataType: 'text',
            success: function (K) {
              var I = K.split('&');
              if (I[0] == '1') {
                var J = G[1].split('#');
                window.parent.close_viewport();
                $('#DataNotFound').html('<p>' + J[1] + '  </p>');
                $('#DataNotFound').dialog({
                  modal: true,
                  buttons: {
                    确定: function () {
                      $('#DataNotFound').html('<p>是否提交贷款申请</p>');
                      $('#DataNotFound').dialog({
                        modal: true,
                        buttons: {
                          是: function () {
                            $(this).dialog('close');
                            window.parent.block_viewport();
                            $.ajax({
                              type: 'POST',
                              url: addRecommendBillUrl,
                              data: {
                                CustomerName: B,
                                IDCardNO: E,
                                Mobile: A,
                                AgentVindicatorID: F,
                                Remark: C,
                                LogonGuid: D
                              },
                              dataType: 'text',
                              success: function (M) {
                                window.parent.close_viewport();
                                var L = M.split('&');
                                if (L[0] == '1') {
                                  $('#inputData').hide();
                                  $('#applySuccess').show()
                                } else {
                                  $('#dialog:ui-dialog').dialog('destroy');
                                  $('#DataNotFound').html('<p>' + L[1] + '  </p>');
                                  $('#DataNotFound').dialog({
                                    modal: true,
                                    buttons: {
                                      关闭: function () {
                                        $(this).dialog('close')
                                      }
                                    }
                                  })
                                }
                              }
                            })
                          },
                          否: function () {
                            $(this).dialog('close')
                          }
                        }
                      })
                    }
                  }
                })
              } else {
                window.parent.close_viewport();
                $('#dialog:ui-dialog').dialog('destroy');
                $('#DataNotFound').html('<p>' + I[1] + '  </p>');
                $('#DataNotFound').dialog({
                  modal: true,
                  buttons: {
                    关闭: function () {
                      $(this).dialog('close')
                    }
                  }
                })
              }
            }
          })
        } else {
          window.parent.close_viewport();
          $('#IDCardError').html(errorImageUrl).show();
          $('#DataNotFound').html('<p>' + G[1] + '  </p>');
          $('#DataNotFound').dialog({
            modal: true,
            buttons: {
              关闭: function () {
                $(this).dialog('close')
              }
            }
          });
          return false
        }
      }
    }
  })
}
function MobileVerify(E, A, B, C, F, D) {
  $.ajax({
    type: 'POST',
    url: recommendBillCheckUrl,
    data: {
      CustomerName: B,
      IDCardNO: E,
      Mobile: A,
      LogonGuid: D,
      BillType: 'A'
    },
    dataType: 'text',
    success: function (I) {
      var G = I.split('&');
      if (I != '') {
        if (G[0] == '1') {
          var H = G[1].split('#');
          window.parent.close_viewport();
          $('#DataNotFound').html('<p>' + H[1] + '  </p>');
          $('#DataNotFound').dialog({
            modal: true,
            buttons: {
              确定: function () {
                $('#DataNotFound').html('<p>是否提交贷款申请</p>');
                $('#DataNotFound').dialog({
                  modal: true,
                  buttons: {
                    是: function () {
                      $(this).dialog('close');
                      window.parent.block_viewport();
                      $.ajax({
                        type: 'POST',
                        url: addRecommendBillUrl,
                        data: {
                          CustomerName: B,
                          IDCardNO: E,
                          Mobile: A,
                          AgentVindicatorID: F,
                          Remark: C,
                          LogonGuid: D
                        },
                        dataType: 'text',
                        success: function (K) {
                          window.parent.close_viewport();
                          var J = K.split('&');
                          if (J[0] != '') {
                            $('#inputData').hide();
                            $('#applySuccess').show()
                          } else {
                            $('#dialog:ui-dialog').dialog('destroy');
                            $('#DataNotFound').html('<p>操作异常！</p>');
                            $('#DataNotFound').dialog({
                              modal: true,
                              buttons: {
                                关闭: function () {
                                  $(this).dialog('close')
                                }
                              }
                            })
                          }
                        }
                      })
                    },
                    否: function () {
                      $(this).dialog('close')
                    }
                  }
                })
              }
            }
          })
        } else {
          window.parent.close_viewport();
          $('#MobileError').html(errorImageUrl).show();
          $('#DataNotFound').html('<p>' + G[1] + '  </p>');
          $('#DataNotFound').dialog({
            modal: true,
            buttons: {
              关闭: function () {
                $(this).dialog('close')
              }
            }
          });
          return false
        }
      } else {
        window.parent.close_viewport();
        $('#DataNotFound').html('<p>操作异常</p>');
        $('#DataNotFound').dialog({
          modal: true,
          buttons: {
            关闭: function () {
              $(this).dialog('close')
            }
          }
        });
        return false
      }
    }
  })
};
